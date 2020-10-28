import React, { Component } from "react";
import { Grid, Row, Button, Alert } from "react-bootstrap";
import FontAwesomeIcon from '@fortawesome/react-fontawesome'
import faCheckSquare from '@fortawesome/fontawesome-free-solid/faCheckSquare'
import faPalette from '@fortawesome/fontawesome-free-solid/faPalette'
import faCheck from '@fortawesome/fontawesome-free-solid/faCheck'
import Config from "../../constant/Config";
import { iconStyle, buttonTextStyle, centerRowContentStyle, centerTitleContentStyle } from "../../constant/Styles"
import $ from "jquery";

class Critic extends Component {
  constructor(props) {
    super(props);
    this.state = {
      images: [],
      words: [],
      voteSubmitted: false
    };
  }

  loadImages = async (roundId) => {
    var criticRes = await fetch(
      `${Config.apiurl}/images?roundId=${roundId}`);
    if (criticRes.status === 200) {
      const images = await criticRes.json();
      this.setState({images: images});
    }
    var wordsRes = await fetch(
      `${Config.apiurl}/words?roomId=${this.props.roomId}&roundId=${roundId}`);
    if (wordsRes.status === 200) {
      const words = await wordsRes.json();
      this.setState({words: words});
    }
  }

  onClickRateImage = async (imageId) => {
    this.onClickRateImageBase(imageId, null);
  }

  onClickRateWord = async (wordId) => {
    this.onClickRateImageBase(null, wordId);
  }

  onClickRateImageBase = async (imageId, wordId) => {
    const rating = {
      raterUserId: this.props.userId,
      roundId: this.props.roundId,
      imageId: imageId,
      wordId: wordId,
      rating: 1
    };
    var ratingRes = await fetch(
      `${Config.apiurl}/rating?${$.param(rating)}`,
      {
        method: "POST"
      })
    if (ratingRes.status === 200) {
      console.log(`Image: ${imageId}/Word: ${wordId} rated by ${this.props.userId}`);
      this.setState({voteSubmitted: true});
    }
  }

  componentWillMount = () => {
    // Map the props to the state
    this.loadImages(this.props.roundId);
  }

  render = () => {
    const yourContentTextContentStyle = {
      ...centerTitleContentStyle,
      margin: 0
    };

    const voteSubmittedStyle = {
      margin: "10px",
      fontSize: "medium"
    };
    const votedElement = (
      <div style={voteSubmittedStyle}>
        <FontAwesomeIcon style={iconStyle} icon={faCheck} />
        <span style={buttonTextStyle}>Vote Submitted!</span>
      </div>);

    return (
      <Grid>
        <Row>
          {this.state.images.map((image) => {
            let maybeButton = image.userId !== this.props.userId
              ? <Button
                  className="button"
                  onClick={e => this.onClickRateImage(image.imageId)}>
                  <FontAwesomeIcon style={iconStyle} icon={faCheckSquare} />
                  <span style={buttonTextStyle}>Vote</span>
                </Button>
              : <div style={yourContentTextContentStyle}>
                  <FontAwesomeIcon style={iconStyle} icon={faPalette} />
                  <span style={buttonTextStyle}>This is your work - aren't you proud.</span>
                </div>;

            if (this.state.voteSubmitted) maybeButton = votedElement;

            return (
              <div key={ image.imageId }>
                <Row style={centerRowContentStyle}>
                  <img src={ image.imageBase64 } />
                </Row>
                <Row style={centerRowContentStyle}>
                  { maybeButton }
                </Row>
              </div>);
          })}
        </Row>
        <Row>
          {this.state.words.map((word) => {

            let maybeButton = word.userId !== this.props.userId
              ? <Button
                  className="button"
                  onClick={e => this.onClickRateWord(word.wordId)}>
                  <FontAwesomeIcon style={iconStyle} icon={faCheckSquare} />
                  <span style={buttonTextStyle}>Vote</span>
                </Button>
              : <div style={yourContentTextContentStyle}>
                  <FontAwesomeIcon style={iconStyle} icon={faPalette} />
                  <span style={buttonTextStyle}>I can't believe you said this</span>
                </div>;

            if (this.state.voteSubmitted) maybeButton = votedElement;

            const alertStyle = {
              padding: "0.5em",
              display: "inline-block",
              marginBottom: 0
            };

            return (
              <div key={ word.wordId }>
                <Row style={centerRowContentStyle}>
                  <Alert style={alertStyle} bsStyle="info">
                    <span>{ word.word }</span>
                  </Alert>
                </Row>
                <Row style={centerRowContentStyle}>
                  { maybeButton }
                </Row>
              </div>);
          })}
        </Row>
      </Grid>
    );
  }
}

export default Critic;