import React, { Component } from 'react';
import { Grid, Col, Row, Button } from 'react-bootstrap'; 
import { connect } from "react-redux";
import Config from '../../constant/Config';
import './Draw.css';
const LC = require('literallycanvas');

class ConnectedDraw extends Component {

  constructor(props) {
    super(props);
    const { userId, roundIdd } = props;
    this.state = {
      user: null,
      round: null
    }
  }

  componentWillReceiveProps = (newProps) => {
    // Map the props to the state
    this.setState({user: newProps.user, round: newProps.round })
  }
  
  async onClickUploadDrawing(e) {
    const drawingDataUrl = this.literallycanvas.lc.getImage().toDataURL();
    const drawingRes = await fetch(
      `${Config.apiurl}/image?userId=${this.state.user.userId}&roundId=${this.state.round.roundId}`, 
      {
        method: 'POST',
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/json"
        },
        body: JSON.stringify({"drawingBase64": drawingDataUrl})
      });

    if (drawingRes.status === 200) {
      console.log("Uploaded drawing")
    }
  }

  render() {
    return (
      <div className="draw">
        <Row>
          <Col>
            <LC.LiterallyCanvasReactComponent 
              imageURLPrefix="/img"
              id="draw-canvas" 
              ref={(c) => this.literallycanvas = c} />
          </Col>
        </Row>
        <Row className="button-row">
          <Col smOffset={3} sm={6}>
            <Button
              className="upload-room-button button"
              onClick={(e) => this.onClickUploadDrawing(e)}
            >
              Upload Drawing
            </Button>
          </Col>
        </Row>
      </div>
    );
  }
}

const mapStateToProps = (state, ownProperties) => {
  // Set the props using the store
  return { user: state.user, round: state.round };
}

const Draw = connect(mapStateToProps)(ConnectedDraw);

export default Draw;