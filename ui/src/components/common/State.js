
import React, { Component } from 'react';
import { connect } from "react-redux";
import { Row } from 'react-bootstrap';
import Config from "../../constant/Config";

class ConnectedState extends Component {
  constructor(props) {
    super(props);
    this.state = {
      room: {
        roomId: null,
        currentRoundId: null
      },
      round: null,
      entries: [],
      minigames: []
    };
  }

  componentWillMount = () => {
    this.prepareComponentState(this.props);
  }

  componentWillReceiveProps = (newProps) => {
    this.prepareComponentState(newProps);
  }

  prepareComponentState = (props) => {
    // Map the props to the state
    this.setState({
      ...props
    });
  }

  render = () => {
    if (!Config.isDebugMode) return null;
    return (
      <div className="state">
        <Row>
          <div>RoomState: { JSON.stringify(this.state.room) } </div>
        </Row>
        <Row>
          <div>RoundState: { JSON.stringify(this.state.round) } </div>
        </Row>
        <Row>
          <div>EntriesState: { JSON.stringify(this.state.entries) } </div>
        </Row>
        <Row>
          <div>MinigamesState: { JSON.stringify(this.state.minigames) } </div>
        </Row>
        <Row>
          <div>UserState: { JSON.stringify(this.state.user) } </div>
        </Row>
      </div>
    );
  }
}

const mapStateToProps = (state, ownProperties) => {
  // Set the props using the store
  return {
    room: state.room,
    round: state.round,
    entries: state.entries,
    minigames: state.minigames,
    user: state.user
  };
}

const State = connect(mapStateToProps)(ConnectedState);

export default State;