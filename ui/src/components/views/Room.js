import React, { Component } from 'react';
import { Grid, Col, Row, Button } from 'react-bootstrap'; 
import { connect } from "react-redux";
import {CopyToClipboard} from 'react-copy-to-clipboard';
import FontAwesomeIcon from '@fortawesome/react-fontawesome'
import faClipboard from '@fortawesome/fontawesome-free-solid/faClipboard'
import Draw from '../common/Draw';
import State from '../common/State';
import RoundInfo from '../common/RoundInfo';
import Critic from '../common/Critic';
import Review from '../common/Review';
import Words from '../common/Words';
import DrawingWord from '../common/DrawingWord';
import RoomUsers from '../common/RoomUsers';
import Config from '../../constant/Config';
import { DRAWING, CRITIQUING, REVIEWING } from '../../constant/StageStateIds';
import './Room.css';
import { iconStyle, buttonTextStyle } from "../../constant/Styles"

class ConnectedRoom extends Component {

  constructor(props) {
    super(props);
    this.state = {
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

  componentWillMount = () => {
    this.prepareComponentState(this.props);
  }

  componentWillReceiveProps = (newProps) => {
    this.prepareComponentState(newProps);
  }

  prepareComponentState = (props) => {
    // Map the props to the state
    this.setState({
      room: { ...props.room }, 
      user: { ...props.user }, 
      round: { ...props.round }
    });
  }

  render() {
    var buttonStyle = {
      display: "inline-block",
      margin: "15px"
    }
    const centerTitleContentStyle = {
      textAlign: "center",
    }
    return (
      <div className="room">
        <Grid>
          <State />
          <div className="container">
            <Row style={centerTitleContentStyle}>
                <Button
                  className="start-round-button button"
                  onClick={e => this.onClickStartRound(e)}
                  style={buttonStyle}>
                  Start Round
                </Button>
            </Row>
            <Row style={centerTitleContentStyle}>
              <CopyToClipboard text={window.location.href}>
                <Button>
                  <FontAwesomeIcon style={iconStyle} icon={faClipboard} />
                  <span style={buttonTextStyle}>Copy link to room to clipboard</span>
                </Button>
              </CopyToClipboard>
            </Row>
          </div>
          <RoomUsers />
          { !this.state.room.currentRoundId && (<Words />)}
          { this.state.room.currentRoundId && (
            <div>
              <RoundInfo />
              <DrawingWord wordId={this.state.round.drawingWordId} />
            </div>
          )}
          { this.state.round.stageStateId === DRAWING && (
            <Draw roundId={ this.state.round.roundId } userId={ this.state.user.userId } />
          )}
          { this.state.round.stageStateId === CRITIQUING && (
            <Critic roundId={ this.state.round.roundId } userId={ this.state.user.userId } />
          )}
          { this.state.round.stageStateId === REVIEWING && (
            <Review roundId={ this.state.round.roundId } />
          )}
        </Grid>
      </div>
    );
  }
}

const mapStateToProps = (state, ownProperties) => {
  // Set the props using the store
  return { room: state.room, user: state.user, round: state.round };
}

const Room = connect(mapStateToProps)(ConnectedRoom);

export default Room;