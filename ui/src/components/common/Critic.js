import React, { Component } from "react";
import { Grid, Row, Button } from "react-bootstrap"; 
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
  }

  onClickRateImage = async (imageId) => {
    const rating = {
      raterUserId: this.props.userId,
      imageId: imageId,
      rating: 1
    };
    var ratingRes = await fetch(
      `${Config.apiurl}/rating?${$.param(rating)}`,
      {
        method: "POST" 
      })
    if (ratingRes.status === 200) {
      console.log(`Image: ${imageId} rated by ${this.props.userId}`);
      this.setState({voteSubmitted: true});
    }
  }

  componentWillMount = () => {
    // Map the props to the state
    this.loadImages(this.props.roundId);
  }

  render = () => {
    if (!this.state.voteSubmitted) {
      return (
        <Grid>
          <Row>
            {this.state.images.map((image) => {
              const yourImageTextContentStyle = {
                ...centerTitleContentStyle,
                margin: 0
              };
              const maybeButton = image.userId !== this.props.userId 
                ? <Button 
                    className="button" 
                    onClick={e => this.onClickRateImage(image.imageId)}> 
                    <FontAwesomeIcon style={iconStyle} icon={faCheckSquare} />
                    <span style={buttonTextStyle}>Vote</span>
                  </Button>
                : <div style={yourImageTextContentStyle}>
                    <FontAwesomeIcon style={iconStyle} icon={faPalette} />
                    <span style={buttonTextStyle}>This is your image - aren't you proud.</span>
                  </div>;

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
        </Grid>
      );
    } else { 
      const voteSubmittedStyle = {
        margin: "10px",
        fontSize: "medium"
      };
      return (
        <Grid>
          <Row style={centerRowContentStyle}>
            <div style={voteSubmittedStyle}>
              <FontAwesomeIcon style={iconStyle} icon={faCheck} />
              <span style={buttonTextStyle}>Vote Submitted!</span>
            </div>
          </Row>
        </Grid>
      );
    }
  }
}

export default Critic;