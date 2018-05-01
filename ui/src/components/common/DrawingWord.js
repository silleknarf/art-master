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
    return <div>Draw: { this.state.word.word }</div>
  }
}

export default DrawingWord;