import React, { Component } from 'react';
import { Grid, Col, Row, Button } from 'react-bootstrap'; 
import Config from '../../constant/Config';
import './Draw.css';

class Draw extends Component {

  constructor(props) {
    super(props);
    const { userId, roundIdd } = props;
    this.state = {
      userId: 1,
      roundId: 1
    }
  }

  componentDidMount() {
    var ctx = this.canvas.getContext("2d");
    ctx.rect(20,20,150,100);
    ctx.stroke();
  }
  
  async onClickUploadDrawing(e) {
    const drawingDataUrl = this.canvas.toDataURL();
    const drawingRes = await fetch(`${Config.apiurl}/image?userId=${this.state.userId}&roundId=${this.state.roundId}`, {
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