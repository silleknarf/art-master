import React, { Component } from 'react';
import { Grid, Col, Row, Button } from 'react-bootstrap'; 
import FontAwesomeIcon from '@fortawesome/react-fontawesome'
import faUpload from '@fortawesome/fontawesome-free-solid/faUpload'
import faCheckSquare from '@fortawesome/fontawesome-free-solid/faCheckSquare'
import Config from '../../constant/Config';
import { iconStyle, buttonTextStyle, centerRowContentStyle, centerTitleContentStyle } from "../../constant/Styles"
import * as LC from "../../../node_modules/literallycanvas/lib/js/index.js"

class Draw extends Component {

  constructor(props) {
    super(props);
    this.state = {
      drawingSubmitted: props.drawingSubmitted || false
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
      this.setState({drawingSubmitted: true});
    }
  }

  render() {
    if (!this.state.drawingSubmitted) {
      return (
        <Grid>
          <Row style={centerRowContentStyle}>
              <LC.LiterallyCanvasReactComponent 
                imageURLPrefix="/img"
                id="draw-canvas" 
                ref={(c) => this.literallycanvas = c} />
          </Row>
          <Row className="button-row" style={centerRowContentStyle}>
              <Button
                className="upload-room-button button"
                onClick={(e) => this.onClickUploadDrawing(e)}
              >
                <FontAwesomeIcon style={iconStyle} icon={faUpload} />
                <span style={buttonTextStyle}>Upload Drawing</span>
              </Button>
          </Row>
        </Grid>
      );
    } else {
      return (
        <div style={centerTitleContentStyle}>
          <FontAwesomeIcon style={iconStyle} icon={faCheckSquare} />
          <span style={buttonTextStyle}>Drawing Submitted!</span>
        </div>
      );
    }
  }
}

export default Draw;