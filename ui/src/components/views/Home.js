import React, { Component } from 'react';
import { Grid, Col, Row, Button, FormControl, FormGroup, HelpBlock, ControlLabel } from 'react-bootstrap'; 
import config from '../../constant/config';
import './Home.css';

class Home extends Component {

  constructor(props) {
    super(props);
    this.state = {
      username: '',
      usernameFeedback: '',
    }
  }

  async onClickCreateRoom(e) {
    e.preventDefault();
    try {
      const { userId, username } = await this.createUser();
      const roomRes = await fetch(`${config.apiurl}/room`, {
        method: 'POST',
      });
      const { roomId, roomCode } = await roomRes.json();
      const res = await fetch(`${config.apiurl}/room/${roomId}/user/${userId}`, {
        method: 'POST',
      });
      if (res.status === 200) {
        this.props.history.push(`/room/${roomCode}`);
      }
    } catch(err) {
      this.setState({
        usernameFeedback: 'Unable to create username', 
      })
    }
  }

  onClickJoinRoom(e) {
    e.preventDefault();
    console.log('join room');
    // TODO: logic to pick username and 
  }

  async createUser() {
    try {
      const res = await fetch(`${config.apiurl}/user/${this.state.username}`, {
        method: 'POST',
      });
      if (res.status === 200) {
        const { userId, username } = await res.json();
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
                  <ControlLabel className="username-label">Username</ControlLabel>
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
