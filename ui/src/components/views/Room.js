import React, { Component } from 'react';
import { Grid, Col, Row, Button } from 'react-bootstrap'; 
import { connect } from "react-redux";
import Draw from '../common/Draw';
import State from '../common/State';
import RoundInfo from '../common/RoundInfo';
import Critic from '../common/Critic';
import Config from '../../constant/Config';
import { DRAWING, CRITIQUING } from '../../constant/StageStateIds';
import './Room.css';

class ConnectedRoom extends Component {

  constructor(props) {
    super(props);
    this.state = {
      gameState: Config.gameStates.PENDING_START,
      room: { currentRoundId: null },
      round: { stageStateId: null }
    }
  }

  onClickStartRound = async (e) => {
    var startRoundRes = await fetch(
      `${Config.apiurl}/round?roomId=${this.state.room.roomId}&userId=${this.state.user.userId}`, 
      { method: "POST" });
    if (startRoundRes.status === 200) {
      console.log(`Starting round for room: ${this.state.room.roomId} on behalf of user: ${this.state.user.userId}`);
    }
  }

  componentWillReceiveProps = (newProps) => {
    // Map the props to the state
    this.setState({
      room: { ...newProps.room }, 
      user: { ...newProps.user }, 
      round: { ...newProps.round }
    });
  }

  render() {
    return (
      <div className="room">
        <Grid>
          <State />
          <Row className="button-row">
            <Col smOffset={3} sm={6}>
              <Button
                className="start-round-button button"
                onClick={e => this.onClickStartRound(e)}
              >
                Start Round
              </Button>
            </Col>
          </Row>
          { this.state.room.currentRoundId && (<RoundInfo />)}
          { this.state.round.stageStateId === DRAWING && (<Draw />)}
          { this.state.round.stageStateId === CRITIQUING && (<Critic />)}
        </Grid>
      </div>
    );
  }
}

const mapStateToProps = (state, ownProperties) => {
  // Set the props using the store
  return { 
    room: state.room, 
    user: state.user, 
    round: state.round 
  };
}

const Room = connect(mapStateToProps)(ConnectedRoom);

export default Room;
