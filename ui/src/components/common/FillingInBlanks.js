import React, { Component } from 'react';
import Config from '../../constant/Config';
import { Grid, Row, Button, Alert } from 'react-bootstrap';
import FontAwesomeIcon from '@fortawesome/react-fontawesome'
import faUpload from '@fortawesome/fontawesome-free-solid/faUpload'
import { iconStyle, buttonTextStyle, centerRowContentStyle, centerTitleContentStyle } from "../../constant/Styles"
import { connect } from "react-redux";
import $ from "jquery";

class ConnectedFillingInBlanks extends Component {

  constructor(props) {
    super(props);
    this.state = {
      entry: {
        entryComponents: [{
          key: "Sentence",
          value: ""
        }]
      },
      sentenceBlanks: [],
      sentenceSubmitted: false
    };
  }

  componentWillMount = () => {
    this.updateComponentState(this.props);
  }

  componentWillReceiveProps = (newProps) => {
    this.updateComponentState(newProps);
  }

  updateComponentState = async (newProps) => {
    if (!newProps) return;

    const gracePeriodDurationInSeconds = 2;
    if (newProps.round.timeRemaining <= gracePeriodDurationInSeconds) {
      this.onClickSubmitText();
    }

    this.setState({
      user: newProps.user,
      room: newProps.room
    });

    const entryId = newProps.entryId;
    if (!entryId) return;
    var entryRes = await fetch(`${Config.apiurl}/entry?entryId=${entryId}`);
    if (entryRes.status === 200) {
      const entry = await entryRes.json();
      this.setState({
        entry
      });
    }
  }

  onChangeSentenceBlank = async (index, e) => {
    const newSentenceBlanks = [ ...this.state.sentenceBlanks ];
    newSentenceBlanks[index] = e.target.value;
    this.setState({ sentenceBlanks: newSentenceBlanks });
  }

  onClickSubmitText = async (e) => {
    const state = this.state;
    const sentence = this.state.entry.entryComponents[0].value
      .split(/_+/)
      .map((s, index) => {
        const blank = state.sentenceBlanks[index];
        return !blank ? s : s + blank;
      })
      .join("");

    const entry = {
      entryComponents: [{
        key: "Sentence",
        value: sentence
      }],
      roomId: this.state.room.roomId,
      roundId: this.state.room.currentRoundId,
      userId: this.state.user.userId
    };
    this.setState({ submittedSentence: sentence });
    const addEntryRes = await fetch(`${Config.apiurl}/entry?${$.param(entry)}`,
      { method: "POST" });
    if (addEntryRes.status === 200) {
      console.log(`Added entry: ${submittedSentence}`);
    }
  }

  render = () => {
    const style = {
      margin: "10px",
      fontSize: "medium"
    };
    const centerContentStyle = {
      paddingLeft: "15px",
      paddingRight: "15px",
      textAlign: "center",
      marginLeft: 0,
      marginRight: 0,
      marginBottom: "5px"
    };
    const gridStyle = {
      paddingLeft: 0,
      paddingRight: 0
    };

    const sentenceBuilderElements = []
    const sentenceContent = this.state.entry.entryComponents[0].value.split(/_+/);
    sentenceContent.forEach((s, index) => {
      sentenceBuilderElements.push(<span key={index*2}>{s}</span>);
      if (index !== sentenceContent.length-1)
        sentenceBuilderElements.push(
          <input type="text"
                key={index*2+1}
                onChange={(e) => {this.onChangeSentenceBlank(index, e)}}></input>
          );
    });

    const alertStyle = {
      padding: "0.5em",
      display: "inline-block",
    };

    const sentenceBuildingComponent = (
      <Grid style={gridStyle}>
        <Row style={centerContentStyle}>
          <div style={style}>
            Fill the blanks in:
          </div>
        </Row>
        <Row style={centerContentStyle}>
          <div style={style}>
            { sentenceBuilderElements }
          </div>
        </Row>
        <Row className="button-row" style={centerRowContentStyle}>
            <Button
              style={centerTitleContentStyle}
              className="upload-room-button button"
              onClick={(e) => this.onClickSubmitText(e)}>
              <FontAwesomeIcon style={iconStyle} icon={faUpload} />
              <span style={buttonTextStyle}>Submit</span>
            </Button>
        </Row>
      </Grid>);

    if (!this.state.submittedSentence) {
      return sentenceBuildingComponent;
    }

    return (
      <Alert style={alertStyle} bsStyle="info">
        <span>{ this.state.submittedSentence }</span>
      </Alert>);
  }
}

const mapStateToProps = (state, ownProperties) => {
  // Set the props using the store
  return { user: state.user, room: state.room, round: state.round };
}

const FillingInBlanks = connect(mapStateToProps)(ConnectedFillingInBlanks);

export default FillingInBlanks;