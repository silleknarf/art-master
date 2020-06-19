import React, { Component } from 'react';
import { Grid, Row, Button, Tabs, Tab, Alert, MenuItem, DropdownButton } from 'react-bootstrap'; 
import { connect } from "react-redux";
import FontAwesomeIcon from '@fortawesome/react-fontawesome'
import faExclamationTriangle from '@fortawesome/fontawesome-free-solid/faExclamationTriangle'
import Draw from '../common/Draw';
import FillingInBlanks from '../common/FillingInBlanks';
import State from '../common/State';
import RoundInfo from '../common/RoundInfo';
import Critic from '../common/Critic';
import Review from '../common/Review';
import Words from '../common/Words';
import DrawingWord from '../common/DrawingWord';
import RoomUsers from '../common/RoomUsers';
import Config from '../../constant/Config';
import { DRAWING, CRITIQUING, REVIEWING, FILLING_IN_BLANKS } from '../../constant/StageStateIds';
import './Room.css';
import { iconStyle, buttonTextStyle, centerRowContentStyle, centerTitleContentStyle, tabsStyle, titleStyle } from "../../constant/Styles"

class ConnectedRoom extends Component {

  constructor(props) {
    super(props);
    this.state = {
      room: { currentRoundId: null },
      round: { stageStateId: null },
      minigames: [],
      previousRoundId: null,
      currentTabIndex: 1
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

  onClickChangeMinigame = async (minigameId) => {
    var startRoundRes = await fetch(
      `${Config.apiurl}/room/${this.state.room.roomId}/minigame/${minigameId}`, 
      { method: "POST" });
    if (startRoundRes.status === 200) {
      console.log(`Changed minigame for room: ${this.state.room.roomId} to: ${minigameId}`);
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
      round: { ...props.round },
      words: [ ...props.words ],
      minigames: [ ...props.minigames ]
    });

    var previousRoundId = this.state.previousRoundId;
    const currentRoundId = props.room && props.room.currentRoundId || null;
    if (!currentRoundId) {
      this.setState({ currentTabIndex: 1 });
    } 
    else if (currentRoundId !== previousRoundId) {
      this.setState({
        previousRoundId: currentRoundId,
        currentTabIndex: 2
      });
    }
  }

  // Required for switching the tabs manually
  handleSelect = (key) => {
    this.setState({ currentTabIndex: key });
  }

  createAlert = (shouldDisplay, text) => {
    const alertStyle = {
      padding: "0.5em",
      display: "inline-block",
      marginBottom: 0
    };

    const alert = shouldDisplay && 
      (<Row style={centerRowContentStyle}>
        <Alert style={alertStyle} bsStyle="warning">
          <FontAwesomeIcon style={iconStyle} icon={faExclamationTriangle} />
          <span style={buttonTextStyle}>{ text}</span>
        </Alert>
      </Row>);
    return alert;
  }

  render() {
    var buttonStyle = {
      display: "inline-block",
      margin: "15px",
      fontSize: "large"
    }
    const areNotEnoughUsers = this.state.room && 
      this.state.room.roomUsers &&
      this.state.room.roomUsers.length < 3;
    const notEnoughUsersText = "Add at least three players before starting the round";
    const notEnoughUsersAlert = this.createAlert(areNotEnoughUsers, notEnoughUsersText);
    
    const areNotEnoughWords = Object.values(this.state.words).length === 0;
    const notEnoughWordsText = "Add at least one word before starting the round";
    const notEnoughWordsAlert = this.createAlert(areNotEnoughWords, notEnoughWordsText); 

    const isRoomOwner = this.state.user &&
      this.state.room &&
      this.state.user.userId == this.state.room.ownerUserId;
    const dropdownItems = this.state.minigames
      .map((minigame) => {
        return <MenuItem as="button" 
                         key={minigame.minigameId}
                         onClick={e => this.onClickChangeMinigame(minigame.minigameId)}>
                { minigame.name }
               </MenuItem>;
      })
    const minigameName = this.state.minigames
      .filter((minigame) => minigame.minigameId === this.state.room.minigameId)
      .map((minigame) => minigame.name)[0] || "";

    return (
      <div className="room">
        <div style={centerTitleContentStyle}> 
          <span style={titleStyle}>Craicbox</span>
        </div>
        <div style={centerTitleContentStyle}> 
          <DropdownButton id="dropdown-item-button" title={minigameName}>
            { dropdownItems }
          </DropdownButton>
        </div>
        <Tabs 
          id="room-tabs"
          style={tabsStyle} 
          activeKey={this.state.currentTabIndex} 
          onSelect={this.handleSelect}>
          <Tab eventKey={1} title="Room">
              <State />
              { isRoomOwner && (<div className="container">
                <Row style={centerTitleContentStyle}>
                  <Button
                    className="start-round-button button"
                    onClick={e => this.onClickStartRound(e)}
                    style={buttonStyle}>
                    Start Round
                  </Button>
                </Row>
                { notEnoughUsersAlert }
                { notEnoughWordsAlert }
              </div>)}
              <Row>
                <div className="col-md-6">
                  <RoomUsers />
                </div>
                <div className="col-md-6">
                  <Words />
                </div>
              </Row>
          </Tab>
          <Tab eventKey={2} title="Round" disabled={!this.state.room.currentRoundId}>
            <Grid>
              <div>
                <RoundInfo />
              </div>
              { this.state.round.stageStateId === DRAWING && (
                <div>
                  <DrawingWord wordId={this.state.round.drawingWordId} />
                  <Draw roundId={ this.state.round.roundId } userId={ this.state.user.userId } />
                </div>
              )}
              { this.state.round.stageStateId === FILLING_IN_BLANKS && (
                <FillingInBlanks wordId={this.state.round.drawingWordId} 
                                 roundId={ this.state.round.roundId } 
                                 userId={ this.state.user.userId } />
              )}
              { this.state.round.stageStateId === CRITIQUING && (
                <Critic roundId={ this.state.round.roundId } 
                        userId={ this.state.user.userId }
                        roomId={ this.state.room.roomId } />
              )}
              { this.state.round.stageStateId === REVIEWING && (
                <Review roundId={ this.state.round.roundId } />
              )}
            </Grid>
          </Tab>
        </Tabs>
      </div>
    );
  }
}

const mapStateToProps = (state, ownProperties) => {
  // Set the props using the store
  return { room: state.room, user: state.user, round: state.round, words: state.words, minigames: state.minigames };
}

const Room = connect(mapStateToProps)(ConnectedRoom);

export default Room;