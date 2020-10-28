import React, { Component } from 'react';
import { Grid, Col, Row, Button, Alert } from 'react-bootstrap';
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
      winningResults: [],
    };
  }

  componentWillMount = async () => {
    const winningResultsRes = await fetch(`${Config.apiurl}/ratings?roundId=${this.state.roundId}`);
    if (winningResultsRes.status === 200) {
      const winningResults = await winningResultsRes.json();
      this.setState({
        winningResults: winningResults
      });
    }
  }

  shouldComponentUpdate = (nextProps, nextState) => {
    return this.state.winningResults.length !== nextState.winningResults.length;
  }

  render = () => {
    const alertStyle = {
      padding: "0.5em",
      display: "inline-block",
      marginBottom: 0
    };

    if (this.state.winningResults.length !== 0) {
      return (
        <Grid>
          {this.state.winningResults.map((winningResult) => {

            const winningResultContent = winningResult.winningImageBase64
              ? <img src={ winningResult.winningImageBase64 }></img>
              : <Alert style={alertStyle} bsStyle="info">
                  <span>{ winningResult.word }</span>
                </Alert>
            return (<div key={ winningResult.winnerId }>
                <Row style={centerRowContentStyle}>
                  { winningResultContent }
                </Row>
                <Row style={centerRowContentStyle}>
                  <FontAwesomeIcon style={iconStyle} icon={faUser} />
                  <span style={buttonTextStyle}>{ winningResult.winnerUsername + ": " + winningResult.votes }</span>
                </Row>
              </div>);
          })}
        </Grid>
        );
    } else {
      return <div>No things were voted for!</div>
    }
  }
}

export default Review;