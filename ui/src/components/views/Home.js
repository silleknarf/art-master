import React, { Component } from 'react';
import { Grid, Col, Row, Button } from 'react-bootstrap'; 
import './Home.css';

class Home extends Component {

  onClickCreateRoom(e) {
    e.preventDefault();
    console.log('create room');
    //TODO: create room request

  }

  onClickJoinRoom(e) {
    e.preventDefault();
    console.log('join room');
    // TODO: logic to pick username and 
  }

  render() {
    return (
      <div className="home">
        <Grid>
          <Row className="input-row">
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
        </Grid>
      </div>
    );
  }
}

export default Home;
