import React, { Component } from 'react';
import { Grid, Col, Row, Button, FormControl, FormGroup } from 'react-bootstrap'; 
import FontAwesomeIcon from '@fortawesome/react-fontawesome'
import faPlus from '@fortawesome/fontawesome-free-solid/faPlus'
import faTrash from '@fortawesome/fontawesome-free-solid/faTrash'
import faFileWord from '@fortawesome/fontawesome-free-solid/faFileWord'
import { connect } from "react-redux";
import Config from '../../constant/Config';
import $ from "jquery";
import { iconStyle, buttonTextStyle, centerRowContentStyle, centerTitleContentStyle } from "../../constant/Styles"

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

  onAddWord = async (e) => {
    const word = {
      word: this.state.newWord,
      roomId: this.state.room.roomId,
      userId: this.state.user.userId
    };
    this.setState({newWord: ""});
    const addWordRes = await fetch(`${Config.apiurl}/word?${$.param(word)}`, 
      { method: "POST" });
    if (addWordRes.status === 200) {
      console.log(`Added word: ${word.word}`);
    }
  }

  onClickRemoveWord = async (wordId) => {
    var word = {
      wordId: wordId
    };
    const removeWordRes = await fetch(`${Config.apiurl}/word?${$.param(word)}`, 
      { method: "DELETE" });
    if (removeWordRes.status === 200) {
      console.log(`Deleted word with id: ${wordId}`);
    }
  }

  onKeyDown = (event: React.KeyboardEvent<HTMLDivElement>) => {
    // 'keypress' event misbehaves on mobile so we track 'Enter' key via 'keydown' event
    if (event.key === 'Enter') {
      event.preventDefault();
      event.stopPropagation();
      this.onAddWord(event);
    }
  }

  render = () => {
    var ulStyle = {
      display: "inline-block"
    };
    const wordStyle = {
      margin: "10px"
    }
    var buttonStyle = {
      display: "inline-block",
      height: "34px",
      marginTop: "-3px"
    }
    return (
      <Grid>
        <Row style={centerTitleContentStyle}>
          <FontAwesomeIcon style={iconStyle} icon={faFileWord} />
          <span style={buttonTextStyle}>Words:</span>
        </Row>
        <Row style={centerRowContentStyle}>
          <ul className="list-group" style={ulStyle}>
            { this.state.words.map((word) => {
              return (
                <li key={word.wordId} className="list-group-item">
                  <span style={wordStyle}>{ word.word }</span>
                  <Button
                    className="remove-word-button btn btn-xs"
                    onClick={(e) => this.onClickRemoveWord(word.wordId)}>
                    <FontAwesomeIcon style={iconStyle} icon={faTrash} />
                  </Button>
                </li>
              );
            })}
          </ul>
        </Row>
        <Row style={centerRowContentStyle}>
          <FormGroup style={ulStyle}>
            <FormControl
              className="word-input"
              type="input"
              onChange={e => this.setState({ newWord: e.target.value })}
              value={this.state.newWord}
              onKeyDown={this.onKeyDown}
            />
          </FormGroup>
          <Button
            className="add-word-button btn"
            onClick={(e) => this.onAddWord(e)}
            style={buttonStyle}>
            <FontAwesomeIcon style={iconStyle} icon={faPlus} />
          </Button>
        </Row>
      </Grid>
    );
  }
}

const mapStateToProps = (state, ownProperties) => {
  // Set the props using the store
  return { words: state.words, user: state.user, room: state.room };
}

const Words = connect(mapStateToProps)(ConnectedWords);

export default Words;