import React, { Component } from 'react';
import { Grid, Col, Row, Button } from 'react-bootstrap'; 
import Draw from '../common/Draw';
import config from '../../constant/config';
import './Room.css';

class Room extends Component {

  constructor(props) {
    super(props);
    this.state = {
      gameState: config.gameStates.PENDING_START,
    }
  }

  render() {
    return (
      <div className="room">
        <Grid>
          <Draw />
        </Grid>
      </div>
    );
  }
}

export default Room;
