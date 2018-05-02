import React, { Component } from 'react';
import { Grid, Col, Row, Button } from 'react-bootstrap'; 
import Config from '../../constant/Config';

class DrawingWord extends Component {
  constructor(props) {
    super(props);
    this.state = { 
      word: { 
        word: ""
      }
    };
  }

  componentDidMount = () => {
    this.updateWord(this.props.wordId);
  }

  updateWord = async(wordId) => {
    var wordRes = await fetch(`${Config.apiurl}/word?wordId=${wordId}`);
    if (wordRes.status === 200) {
      const word = await wordRes.json();
      this.setState({word: word});
    }
  }

  render = () => {
    const style = {
      margin: "10px"
    };
    const rowStyle = {
      textAlign: "center"
    };
    return (
      <div style={rowStyle}>
        <div style={style}>
          🎨 Artists, it's time to draw! You have to draw <strong>{ this.state.word.word }</strong>
        </div>
      </div>
    );
  }
}

export default DrawingWord;