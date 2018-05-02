import React, { Component } from 'react';
import { Grid, Col, Row, Button, FormControl, FormGroup } from 'react-bootstrap'; 
import { connect } from "react-redux";
import Config from '../../constant/Config';
import $ from "jquery";

class ConnectedWords extends Component {
  constructor(props) {
    super(props);
    this.state = { 
      words: [],
      user: null,
      room: null,
      newWord: ""
    };
  }

  componentWillMount = () => {
    this.updateComponentState(this.props);
  }

  componentWillReceiveProps = (newProps) => {
    this.updateComponentState(newProps);
  }

  updateComponentState = (newProps) => {
    if (!newProps) return;
    this.setState({ 
      words: newProps.words, 
      user: newProps.user,
      room: newProps.room
    });
  }

  onClickAddWord = async (e) => {
    const word = {
      word: this.state.newWord,
      roomId: this.state.room.roomId,
      userId: this.state.user.userId
    };
    this.state.newWord = ""
    const addWordRes = await fetch(`${Config.apiurl}/word?${$.param(word)}`, 
      { method: "POST" });
    if (addWordRes.status == 200) {
      console.log(`Added word: ${word.word}`);
    }
  }

  onClickRemoveWord = async (wordId) => {
    var word = {
      wordId: wordId
    };
    const removeWordRes = await fetch(`${Config.apiurl}/word?${$.param(word)}`, 
      { method: "DELETE" });
    if (removeWordRes.status == 200) {
      console.log(`Deleted word with id: ${wordId}`);
    }
  }

  render = () => {
    return (
      <div>
        <Row>
          <ul className="list-group">
            { this.state.words.map((word) => {
              return (
                <li key={word.wordId} className="list-group-item">
                  { word.word }
                  <Button
                    className="remove-word-button button"
                    onClick={(e) => this.onClickRemoveWord(word.wordId)}>
                    Remove Word
                  </Button>
                </li>
              );
            })}
          </ul>
        </Row>
        <Row>
          <FormGroup>
            <FormControl
              className="word-input"
              type="input"
              onChange={e => this.setState({ newWord: e.target.value })}
              value={this.state.newWord}
            />
          </FormGroup>
          <Button
            className="add-word-button button"
            onClick={(e) => this.onClickAddWord(e)}>
            Add Word
          </Button>
        </Row>
      </div>
    );
  }
}

const mapStateToProps = (state, ownProperties) => {
  // Set the props using the store
  return { words: state.words, user: state.user, room: state.room };
}

const Words = connect(mapStateToProps)(ConnectedWords);

export default Words;