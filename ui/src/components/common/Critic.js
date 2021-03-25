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
      entries: [],
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
    var entriesRes = await fetch(
      `${Config.apiurl}/entries?roomId=${this.props.roomId}&roundId=${roundId}`);
    if (entriesRes.status === 200) {
      const entries = await entriesRes.json();
      this.setState({entries: entries});
    }
  }

  onClickRateImage = async (imageId) => {
    this.onClickRateImageBase(imageId, null);
  }

  onClickRateEntry = async (entryId) => {
    this.onClickRateImageBase(null, entryId);
  }

  onClickRateImageBase = async (imageId, entryId) => {
    const rating = {
      raterUserId: this.props.userId,
      roundId: this.props.roundId,
      imageId: imageId,
      entryId: entryId,
      rating: 1
    };
    var ratingRes = await fetch(
      `${Config.apiurl}/rating?${$.param(rating)}`,
      {
        method: "POST"
      })
    if (ratingRes.status === 200) {
      console.log(`Image: ${imageId}/Entry: ${entryId} rated by ${this.props.userId}`);
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
          {this.state.entries.map((entry) => {

            let maybeButton = entry.userId !== this.props.userId
              ? <Button
                  className="button"
                  onClick={e => this.onClickRateEntry(entry.entryId)}>
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
              <div key={ entry.entryId }>
                <Row style={centerRowContentStyle}>
                  <Alert style={alertStyle} bsStyle="info">
                    <span>{ entry.entryComponents[0].value }</span>
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