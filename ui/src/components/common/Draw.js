import React, { Component } from 'react';
import { Grid, Col, Row, Button } from 'react-bootstrap'; 
import config from '../../constant/config';
import './Draw.css';

class Draw extends Component {

  constructor(props) {
    super(props);
    const { userId, roundIdd } = props;
    this.state = {
      userId: userId,
      roundId: roundId
    }
  }
  
  async onClickUploadDrawing(e) {
    const drawingDataUrl = this.canvas.toDataURL();
    const drawingRes = await fetch(`${config.apiurl}/image?userId=${this.state.userId}&roundId=${this.state.roundId}`, {
        method: 'POST',
        body: JSON.stringify({"drawingBase64": drawingDataUrl})
      });
    if (res.status === 200) {
      console.log("Uploaded drawing")
    }
  }

  render() {
    return (
      <div className="draw">
        <Row>
          <Col>
            <canvas id="draw-canvas" ref={(c) => this.canvas = c}>
            </canvas>
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

export default Draw;