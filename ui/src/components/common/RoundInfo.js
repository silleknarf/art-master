import React, { Component } from 'react';
import { Grid, Col, Row, Button } from 'react-bootstrap'; 
import { connect } from "react-redux";

class ConnectedRoundInfo extends Component {
  constructor(props) {
    super(props);
    this.state = {
      round: { timeRemaining: null }
    }
  }

  componentWillMount = () => {
    this.updateComponentState(this.props);
  }

  componentWillReceiveProps = (newProps) => {
    this.updateComponentState(newProps);
  }

  updateComponentState = (newProps) => {
    if (!newProps.round)
      return;
    const roundStateDescriptions = [
      "Drawing", 
      "Critiquing", 
      "Reviewing", 
      "Done"
    ];
    const roundStateDescription = roundStateDescriptions[newProps.round.stageStateId];
    // Map the props to the state
    this.setState({ 
      round: newProps.round, 
      roundStateDescription: roundStateDescription
    });
  }

  render = () => {
    const style = {
      margin: "10px"
    };
    const rowStyle = {
      textAlign: "center"
    };
    return (
      <Grid>
        <Row style={rowStyle}>
          <div style={style}>
            { this.state.roundStateDescription }
          </div>
        </Row>
        <Row style={rowStyle}>
          <div style={style}>
            Time Remaining: { this.state.round.timeRemaining }
          </div>
        </Row>
      </Grid>
    );
  }
}

const mapStateToProps = (state, properties) => {
  return { round: state.round };
}

const RoundInfo = connect(mapStateToProps)(ConnectedRoundInfo);
export default RoundInfo;