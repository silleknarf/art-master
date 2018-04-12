import React, { Component } from 'react';
import { Grid, Col, Row, Button, FormControl, FormGroup, HelpBlock, ControlLabel } from 'react-bootstrap'; 
import config from '../../constant/config';
import './Home.css';

class Home extends Component {

  constructor(props) {
    super(props);
    this.state = {
      roomCode: '',
      username: '',
      usernameFeedback: '',
    }
  }

  async onClickCreateRoom(e) {
    e.preventDefault();
    try {
      const { userId, username } = await this.createUser();
      console.log(`Creating room for user: ${userId}`);
      const roomRes = await fetch(`${config.apiurl}/room?userId=${userId}`, {
        method: 'POST',
      });
      
      if (roomRes.status === 200) {
        const { roomId, roomCode } = roomRes.json();
        console.log(`Created room: ${roomCode}`);
        this.props.history.push(`/room/${roomCode}`);
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

  async onClickJoinRoom(e) {
    e.preventDefault();
    
    // TODO: logic to pick username and 
    const { userId, username } = await this.createUser();
    console.log(`User: ${username} is attempting to join room: ${this.state.roomCode}`);
    
    try {
      const roomRes = await fetch(`${config.apiurl}/room?roomCode=${this.state.roomCode}`, { method: 'GET' });
      const { roomId } = await roomRes.json();
      const res = await fetch(`${config.apiurl}/room/${roomId}/user/${userId}`, {method: 'POST'});
      if (res.status === 200) {
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
      const res = await fetch(`${config.apiurl}/user/${this.state.username}`, {
        method: 'POST',
      });
      if (res.status === 200) {
        const { userId, username } = await res.json();
        console.log(`Created user: ${username}`)
        return { userId, username };
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

  render() {
    return (
      <div className="home">
        <Grid>
          <div className="input-block">
            <Row className="input-row">
              <Col smOffset={3} sm={6}>
                <FormGroup validationState={!this.state.usernameFeedback ? null : 'error'}>
                  <ControlLabel className="label">Username</ControlLabel>
                  <FormControl
                    className="username-input"
                    type="input"
                    onChange={e => this.setState({ username: e.target.value, usernameFeedback: '' })}
                    value={this.state.username}
                  />
                  {this.state.usernameFeedback  && <HelpBlock>{this.state.usernameFeedback}</HelpBlock>}
                </FormGroup>
              </Col>
            </Row>
             <Row className="input-row">
              <Col smOffset={3} sm={6}>
                <FormGroup>
                  <ControlLabel className="label">Room Code</ControlLabel>
                  <FormControl
                    className="room-code-input"
                    type="input"
                    onChange={e => this.setState({ roomCode: e.target.value })}
                    value={this.state.roomCode}
                  />
                </FormGroup>
              </Col>
            </Row>
            <Row className="button-row">
              <Col smOffset={3} sm={6}>
                <Button
                  className="create-room-button button"
                  onClick={(e) => this.onClickCreateRoom(e)}
                >
                  Create Room
                </Button>
                <Button
                  className="join-room-button button"
                  onClick={e => this.onClickJoinRoom(e)}
                >
                  Join Room
                </Button>
              </Col>
            </Row>
          </div>
        </Grid>
      </div>
    );
  }
}

export default Home;