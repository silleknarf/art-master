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

  componentWillReceiveProps = (newProps) => {
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
    return (
      <div>
        <Row>
          <div>
            { this.state.roundStateDescription }
          </div>
        </Row>
        <Row>
          <div>
            Time Remaining: { this.state.round.timeRemaining }
          </div>
        </Row>
      </div>
    );
  }
}

const mapStateToProps = (state, properties) => {
  return { round: state.round };
}

const RoundInfo = connect(mapStateToProps)(ConnectedRoundInfo);
export default RoundInfo;