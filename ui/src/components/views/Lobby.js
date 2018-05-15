import React, { Component } from 'react';
import { Grid, Col, Row, Button, FormControl, FormGroup, HelpBlock, ControlLabel, Tabs, Tab } from 'react-bootstrap'; 
import Config from '../../constant/Config';
import store from '../../redux/Store';
import { updateRoomState, updateRoundState, updateUserState } from "../../redux/Actions";
import './Lobby.css';

class Lobby extends Component {

  constructor(props) {
    super(props);
    this.state = {
      roomCode: "",
      username: "",
      usernameFeedback: "",
      tabIndex: 1
    }
  }

  async onCreateRoom(e) {
    e.preventDefault();
    try {
      const { userId, username } = await this.createUser();
      console.log(`Creating room for user: ${userId}`);
      const roomRes = await fetch(`${Config.apiurl}/room?userId=${userId}`, {
        method: 'POST',
      });
      
      if (roomRes.status === 200) {
        const room = await roomRes.json();
        console.log(`Created room: ${room.roomCode}`);
        this.props.history.push(`/room/${room.roomCode}`);
        localStorage.setItem("roomId", room.roomId);
        store.dispatch(updateRoomState(room));
      } else {
        throw new Error("room creation failed")
      }
    } catch(err) {
      console.log(err);
      this.setState({
        usernameFeedback: 'Unable to create room', 
      });
    }
  }

  async onJoinRoom(e) {
    e.preventDefault();
    
    // TODO: logic to pick username and 
    const { userId, username } = await this.createUser();
    console.log(`User: ${username} is attempting to join room: ${this.state.roomCode}`);
    
    try {
      const roomRes = await fetch(`${Config.apiurl}/room?roomCode=${this.state.roomCode}`, { method: 'GET' });
      const room = await roomRes.json();
      const res = await fetch(`${Config.apiurl}/room/${room.roomId}/user/${userId}`, {method: 'POST'});
      if (res.status === 200) {
        localStorage.setItem("roomId", room.roomId);
        store.dispatch(updateRoomState(room));
        console.log(`Added user: ${username} to room: ${this.state.roomCode}`);
        this.props.history.push(`/room/${this.state.roomCode}`);
      } else {
        throw new Error('Joining the room failed');
      }
    } catch(err) {
      console.log(err.message);
      this.setState({
        usernameFeedback: 'Joining the room failed',
      })
    }
  }

  async createUser() {
    try {
      console.log(`Creating user: ${this.state.username}`);
      const res = await fetch(`${Config.apiurl}/user/${this.state.username}`, {
        method: 'POST',
      });
      if (res.status === 200) {
        var user = await res.json();
        console.log(`Created user: ${user.username}`);
        localStorage.setItem("userId", user.userId);
        store.dispatch(updateUserState(user));
        return user;
      } else {
        throw new Error('username creation failed');
      }
    } catch(err) {
      console.log(err.message);
      this.setState({
        usernameFeedback: 'Unable to create user',
      })
    }
  }

  onKeyDown = (event: React.KeyboardEvent<HTMLDivElement>) => {
    // 'keypress' event misbehaves on mobile so we track 'Enter' key via 'keydown' event
    if (event.key === 'Enter') {
      event.preventDefault();
      event.stopPropagation();
      if (this.state.tabIndex === 1)
        this.onCreateRoom(event);
      else
        this.onJoinRoom(event);
    }
  }

  handleSelect = (key) => {
    this.setState({ tabIndex: key });
  }

  componentDidMount = () => {
    const roomCode = this.getUrlParam("roomCode");
    if (roomCode)
      this.setState({ 
        tabIndex: 2,
        roomCode: roomCode
      });
  }

  getUrlParam = (name) => {
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results)
      return results[1] || "";
    return "";
  }

  render() {
    const shrinkWrapStyle = {
      display: "inline-block",
      width: "min-content",
    };
    const ulStyle = {
      display: "inline-block"
    };

    const usernameRow = (
      <Row className="input-row">
        <Col smOffset={3} sm={6}>
          <FormGroup validationState={!this.state.usernameFeedback ? null : 'error'}>
            <ControlLabel className="label">Username</ControlLabel>
            <FormControl
              className="username-input"
              type="input"
              onChange={e => this.setState({ username: e.target.value, usernameFeedback: '' })}
              value={this.state.username}
              onKeyDown={this.onKeyDown}
            />
            {this.state.usernameFeedback  && <HelpBlock>{this.state.usernameFeedback}</HelpBlock>}
          </FormGroup>
        </Col>
      </Row>
    );
    return (
      <div className="lobby">
        <Tabs 
          id="lobby-tabs" 
          activeKey={this.state.tabIndex} 
          style={ulStyle} 
          onSelect={this.handleSelect}>
          <Tab eventKey={1} title="Create Room">
            <Grid>
              { usernameRow }
              <Row className="button-row">
                <Col smOffset={3} sm={6}>
                  <Button
                    className="create-room-button button"
                    onClick={(e) => this.onCreateRoom(e)}>
                    Create Room
                  </Button>
                </Col>
              </Row>
            </Grid>
          </Tab>
          <Tab eventKey={2} title="Join Room">
            <Grid>
              <Row className="input-row">
                <Col smOffset={3} sm={6}>
                  <FormGroup>
                    <ControlLabel className="label">Room Code</ControlLabel>
                    <FormControl
                      className="room-code-input"
                      type="input"
                      onChange={e => this.setState({ roomCode: e.target.value })}
                      value={this.state.roomCode}
                      onKeyDown={this.onKeyDown}
                    />
                  </FormGroup>
                </Col>
              </Row>
              { usernameRow }
              <Row className="button-row">
                <Col smOffset={3} sm={6}>
                  <Button
                    className="join-room-button button"
                    onClick={e => this.onJoinRoom(e)}>
                    Join Room
                  </Button>
                </Col>
              </Row>
            </Grid>
          </Tab>
        </Tabs>
      </div>
    );
  }
}

export default Lobby;