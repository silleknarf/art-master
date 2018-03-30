import React, { Component } from 'react';
import { Grid, Col, Row, Button } from 'react-bootstrap'; 
import config from '../../constant/config';
import './Draw.css';

class Draw extends Component {

  constructor(props) {
    super(props);
    this.state = {
      drawing: null,
    }
  }

  render() {
    return (
      <div className="draw">
        <canvas id="draw-canvas">
        </canvas>
      </div>
    );
  }
}

export default Draw;
