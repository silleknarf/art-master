import React, { Component } from 'react';
import { Grid, Col, Row, Button } from 'react-bootstrap'; 
import Config from '../../constant/Config';
import './Draw.css';
const LC = require('literallycanvas');

class Draw extends Component {

  constructor(props) {
    super(props);
    const { userId, roundIdd } = props;
    this.state = {
      drawingSubmitted: false
    }
  }

  async onClickUploadDrawing(e) {
    const drawingDataUrl = this.literallycanvas.lc.getImage().toDataURL();
    const drawingRes = await fetch(
      `${Config.apiurl}/image?userId=${this.props.userId}&roundId=${this.props.roundId}`, 
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
      this.state.drawingSubmitted = true;
    }
  }

  render() {
    if (!this.state.drawingSubmitted) {
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
    } else {
      return (
        <div>Drawing Submitted!</div>
      );
    }
  }
}

export default Draw;