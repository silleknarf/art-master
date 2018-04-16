
import React, { Component } from 'react';
import config from '../../constant/config';
import { Grid, Col, Row } from 'react-bootstrap'; 

class State extends Component {
  constructor(props) {
    super(props);
    this.state = {
      room: {
        roomId: 2,
        currentRoundId: null
      },
      round: null
    };
  }

  roomTick = async () => {
    const roomStateRes = await fetch(`${config.apiurl}/room?roomId=${this.state.room.roomId}`);
    if (roomStateRes.status === 200) {
        const roomState = await roomStateRes.json();
        this.setState({ room: { ...roomState }});
    }
  }

  roundTick = async () => {
    if (this.state.room.currentRoundId === null) {
      this.setState({ round: null });
      return;
    }

    const roundStateRes = await fetch(`${config.apiurl}/round?roundId=${this.state.room.currentRoundId}`)
    if (roundStateRes.status === 200) {
        const roundState = await roundStateRes.json();
        this.setState({ round: { ...roundState }});
    }
  }

  componentDidMount = () => {
    this.roomInterval = setInterval(this.roomTick, 1000);
    this.roundInterval = setInterval(this.roundTick, 1000);
  }

  componentWillUnmount = () => {
    clearInterval(this.roomInterval);
    clearInterval(this.roundInterval);
  }

  render = () => {
    return ( 
      <div className="state">
        <Row>
          <div>RoomState: { JSON.stringify(this.state.room) } </div>
        </Row>
        <Row>
          <div>RoundState: { JSON.stringify(this.state.round) } </div>
        </Row>
      </div>
    );
  }
}

export default State;