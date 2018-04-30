import React, { Component } from "react";
import { Grid, Col, Row, Button } from "react-bootstrap"; 
import Config from "../../constant/Config";
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
        <Row>
          {this.state.images.map((image) => {
            return (
              <div key={ image.imageId }>
                <Row>
                  <img src={ "/data/" + image.location } />
                </Row>
                <Row>
                  <Button 
                    className="button" 
                    onClick={e => this.onClickRateImage(image.imageId)}> 
                    Vote
                  </Button>
                </Row>
              </div>);
          })}
        </Row>
      );
    } else { 
      return (
        <Row>
          <div>Vote Submitted!</div>
        </Row>
      );
    }
  }
}

export default Critic;