import React, { Component } from 'react';
import { Grid, Col, Row, Button } from 'react-bootstrap';
import { connect } from "react-redux";
import Display from "seven-segment-display";
import './RoundInfo.css';

class ConnectedRoundInfo extends Component {
  constructor(props) {
    super(props);
    this.state = {
      adjustedTimeRemaining: null
    }
    this.timerId = null;
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

    const isGracePeriodState = newProps.round.stageStateId === 0 || newProps.round.stageStateId === 1;
    const initalTimeRemaining = isGracePeriodState 
      ? newProps.round.timeRemaining - 2 
      : newProps.round.timeRemaining;
    const initialState = this.getStateUpdate(newProps, initalTimeRemaining)
    this.setState(initialState);
    
    if (this.timerId)
      clearInterval(this.timerId);
    this.timerId = setInterval(() => {
      this.setState((prevState) => {
        return this.getStateUpdate(newProps, prevState.adjustedTimeRemaining - 1);
      });
    }, 1000);
  }

  componentWillUnmount = () => {
    if (this.timerId)
      clearInterval(this.timerId);
  }

  getStateUpdate = (newProps, timeRemaining) => {
    const roundStateDescriptions = [
      "Drawing",
      "Fill in the blanks",
      "Critiquing",
      "Reviewing",
      "Done"
    ];
    const roundStateDescription = roundStateDescriptions[newProps.round.stageStateId];
    const adjustedTimeRemaining = Math.max(timeRemaining, 0);

    const timeRemainingDigits = adjustedTimeRemaining
      .toFixed(0)
      .toString()
      .length;
    return {
      timeRemainingDigits,
      roundStateDescription,
      adjustedTimeRemaining
    };
  }

  render = () => {
    const roundStateStyle = {
      color: "white",
      margin: "10px",
      fontSize: "2em",
      textTransform: "uppercase",
      textShadow: "-1px 0 rgb(77, 77, 77), 0 1px rgb(77, 77, 77), 1px 0 rgb(77, 77, 77), 0 -1px rgb(77, 77, 77)"
    };
    const rowStyle = {
      textAlign: "center"
    };
    const timeRemainingStyle = {
      display: "inline-block",
      verticalAlign: "top",
      height: "30px",
      lineHeight: "30px",
      fontSize: "medium"
    };
    const displayStyle = {
      display: "inline-block",
      padding: "5px"
    };

    var display = null;

    if (this.state.adjustedTimeRemaining) {
      display = (<div
        style={displayStyle}
        className="display">
        <Display
          value={this.state.adjustedTimeRemaining.toFixed(0)}
          color="black"
          digitCount={this.state.timeRemainingDigits} />
      </div>);
    }

    return (
      <Grid>
        <Row style={rowStyle}>
          <div style={roundStateStyle}>
            { this.state.roundStateDescription }
          </div>
        </Row>
        <Row style={rowStyle}>
          <div style={timeRemainingStyle}>
            Time Remaining:
          </div>
          { display }
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