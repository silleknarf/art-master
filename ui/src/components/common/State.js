
import React, { Component } from 'react';
import { connect } from "react-redux";
import { Grid, Col, Row } from 'react-bootstrap'; 
import Config from '../../constant/Config';
import store from "../../redux/Store";
import { updateRoomState, updateRoundState } from "../../redux/Actions";

window.store = store;

class ConnectedState extends Component {
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
    const roomStateRes = await fetch(`${Config.apiurl}/room?roomId=${this.state.room.roomId}`);
    if (roomStateRes.status === 200) {
        const roomState = await roomStateRes.json();
        store.dispatch(updateRoomState(roomState));
    }
  }

  roundTick = async () => {
    if (this.state.room.currentRoundId === null) {
      store.dispatch(updateRoundState(null));
      return;
    }

    const roundStateRes = await fetch(`${Config.apiurl}/round?roundId=${this.state.room.currentRoundId}`)
    if (roundStateRes.status === 200) {
        const roundState = await roundStateRes.json();
        store.dispatch(updateRoundState(roundState));
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

  componentWillReceiveProps = (newProps) => {
    // Map the props to the state
    this.setState({room: newProps.room, round: newProps.round })
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

const mapStateToProps = (state, ownProperties) => {
  // Set the props using the store
  return { room: state.room, round: state.round };
}

const State = connect(mapStateToProps)(ConnectedState);

export default State;