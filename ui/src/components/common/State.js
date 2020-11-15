
import React, { Component } from 'react';
import { connect } from "react-redux";
import { Row } from 'react-bootstrap';
import Config from '../../constant/Config';
import store from "../../redux/Store";
import { updateRoomState, updateRoundState, updateWordsState, updateMinigamesState } from "../../redux/Actions";
import io from "socket.io-client";

window.store = store;
window.io = io;

class ConnectedState extends Component {
  constructor(props) {
    super(props);
    this.state = {
      room: {
        roomId: null,
        currentRoundId: null
      },
      round: null,
      words: [],
      minigames: []
    };
  }

  loadRoom = async (socket) => {
    if (this.state.room) {
      const roomStateRes = await fetch(`${Config.apiurl}/room?roomId=${this.state.room.roomId}`);
      if (roomStateRes.status === 200) {
          const roomState = await roomStateRes.json();
          store.dispatch(updateRoomState(roomState));
      }
    }
    socket.on('room', (roomState) => {
      store.dispatch(updateRoomState(roomState));
    });
  }

  loadRound = async (socket) => {
    if (this.state.room && this.state.room.currentRoundId) {
      const roundStateRes = await fetch(`${Config.apiurl}/round?roundId=${this.state.room.currentRoundId}`)
      if (roundStateRes.status === 200) {
          const roundState = await roundStateRes.json();
          store.dispatch(updateRoundState(roundState));
      }
    } else {
      store.dispatch(updateRoundState(null));
    }
    socket.on('round', (roundState) => {
      store.dispatch(updateRoundState(roundState));
    });
  }

  loadWords = async (socket) => {
    if (this.state.room && !this.state.room.currentRoundId) {
      const wordsStateRes = await fetch(`${Config.apiurl}/words?roomId=${this.state.room.roomId}`)
      if (wordsStateRes.status === 200) {
          const wordsState = await wordsStateRes.json();
          store.dispatch(updateWordsState(wordsState));
      }
    }
    socket.on('words', (wordsState) => {
      store.dispatch(updateWordsState(wordsState));
    });
  }

  loadMinigames = async () => {
    const minigamesRes = await fetch(`${Config.apiurl}/minigames`)
    if (minigamesRes.status === 200) {
        const minigamesState = await minigamesRes.json();
        store.dispatch(updateMinigamesState(minigamesState));
    }
  }

  componentDidMount = () => {
    const socket = io(Config.apiurl);
    if (this.state.room && this.state.room.roomId) {
      socket.emit("join", this.state.room.roomId);
    }
    this.loadRoom(socket);
    this.loadRound(socket);
    this.loadWords(socket);
    this.loadMinigames();
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
          <div>WordsState: { JSON.stringify(this.state.words) } </div>
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
    words: state.words,
    minigames: state.minigames,
    user: state.user
  };
}

const State = connect(mapStateToProps)(ConnectedState);

export default State;