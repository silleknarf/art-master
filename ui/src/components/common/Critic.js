import React, { Component } from 'react';
import { Grid, Col, Row, Button } from 'react-bootstrap'; 
import { connect } from "react-redux";
import Config from '../../constant/Config';

class ConnectedCritic extends Component {
  constructor(props) {
    super(props);
    this.state = {
      images: [],
      round: {},
      voteSubmitted: false
    };
  }

  loadImages = async (round) => {
    if (!this.state.round.roundId) {
      return;
    }
    var criticRes = await fetch(
      `${Config.apiurl}/images?roundId=${this.state.round.roundId}`);
    if (criticRes.status === 200) {
      this.state.images = await criticRes.json();
    }
  }

  onClickRateImage = async (imageId) => {
    var ratingRes = await fetch(
      `${Config.apiurl}/rating?raterUserId=${this.state.user.userId}&imageId=${imageId}&rating=1`,
      {
        method: "POST" 
      })
    if (ratingRes.status === 200) {
      console.log(`Image: ${imageId} rated by ${this.state.user.userId}`);
      this.state.voteSubmitted = true;
    }
  }

  componentWillReceiveProps = (newProps) => {
    // Map the props to the state
    this.loadImages(newProps.round);
    this.setState({ 
      round: newProps.round, 
      user: newProps.user 
    });
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

  const mapStateToProps = (state, ownProperties) => {
  // Set the props using the store
  return { round: state.round, user: state.user };
}

const Critic = connect(mapStateToProps)(ConnectedCritic);

export default Critic;