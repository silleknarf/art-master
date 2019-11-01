import React, { Component } from 'react';
import { Grid, Col, Row, Button } from 'react-bootstrap'; 
import FontAwesomeIcon from '@fortawesome/react-fontawesome'
import faUser from '@fortawesome/fontawesome-free-solid/faUser'
import { connect } from "react-redux";
import Config from '../../constant/Config';
import { iconStyle, buttonTextStyle, centerRowContentStyle } from "../../constant/Styles"

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
        <Grid>
          {this.state.winningImages.map((winningImage) => {
            return (<div key={ winningImage.winnerId }>
                <Row style={centerRowContentStyle}>
                  <img src={ winningImage.winningImageBase64 }></img>
                </Row>
                <Row style={centerRowContentStyle}>
                  <FontAwesomeIcon style={iconStyle} icon={faUser} />
                  <span style={buttonTextStyle}>{ winningImage.winnerUsername }</span>
                </Row>
              </div>);
          })}
        </Grid>
        );
    } else { 
      return <div>No images were voted for!</div>
    }
  }
}

export default Review;