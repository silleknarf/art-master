import React, { Component } from 'react';
import { Grid, Col, Row, Button } from 'react-bootstrap'; 
import { connect } from "react-redux";
import Config from '../../constant/Config';

class Review extends Component {
  constructor(props) {
    super(props);
    this.state = {
      roundId: props.roundId,
      winningImages: [],
    };
  }
  
  componentWillMount = async () => {
    const winningImagesRes = await fetch(`${Config.apiurl}/ratings?roundId=${this.state.roundId}`);
    if (winningImagesRes.status === 200) {
      const winningImages = await winningImagesRes.json();
      this.setState({ 
        winningImages: winningImages
      });
    }
  }
  
  shouldComponentUpdate = (nextProps, nextState) => {
    return this.state.winningImages.length !== nextState.winningImages.length;
  }

  
  render = () => {
    if (this.state.winningImages.length !== 0) {
      return (
        <div>
          {this.state.winningImages.map((winningImage) => {
            return (<div key={ winningImage.winnerId }>
                <Row>
                  <img src={ "/data/" + winningImage.winningImageLocation }></img>
                </Row>
                <Row>
                  <div>{ winningImage.winnerUsername }</div>
                </Row>
              </div>);
          })}
        </div>
        );
    } else { 
      return <div>No images were voted for!</div>
    }
  }
}

export default Review;