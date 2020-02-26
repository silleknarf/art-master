import React, { Component } from 'react';
import { Grid, Col, Row, Button } from 'react-bootstrap'; 
import FontAwesomeIcon from '@fortawesome/react-fontawesome'
import faUser from '@fortawesome/fontawesome-free-solid/faUser'
import faUsers from '@fortawesome/fontawesome-free-solid/faUsers'
import faClipboard from '@fortawesome/fontawesome-free-solid/faClipboard'
import { connect } from "react-redux";
import Config from '../../constant/Config';
import { iconStyle, buttonTextStyle, centerRowContentStyle, centerTitleContentStyle } from "../../constant/Styles"
import {CopyToClipboard} from 'react-copy-to-clipboard';

class ConnectedRoomUsers extends Component {
  constructor(props) {
    super(props);
    this.state = {
      room: { roomUsers: [] },
      user: { userId: null}
    };
  }

  componentWillReceiveProps = (newProps) => {
    this.updateComponentState(newProps);
  }

  componentWillMount = () => {
    this.updateComponentState(this.props);
  }

  updateComponentState(newProps) {
    if (!newProps.room || !newProps.room.roomUsers || !newProps.user)
      return;
    this.setState({room: newProps.room, user: newProps.user });
  }

  render = () => {
    var ulStyle = {
      display: "inline-block"
    };
    var gridStyle = {
      width: "initial"
    };

    const currentUserTextStyle = {
      fontWeight: "bold",
      margin: "2px"
    };
    
    const joinRoomUrl = window.location.hostname + 
      "/?roomCode=" + 
      this.state.room.roomCode;
    return (
      <Grid style={gridStyle}>
        <Row style={centerTitleContentStyle}>
          <FontAwesomeIcon style={iconStyle} icon={faUsers} />
          <span style={buttonTextStyle}>Players in room:</span>
        </Row>
        <Row style={centerRowContentStyle}>
          <ul className="list-group" style={ulStyle}>
            {this.state.room.roomUsers.map((roomUser) => {
              return (
                <li key={roomUser.userId} className="list-group-item">
                  <FontAwesomeIcon style={iconStyle} icon={faUser} />
                  { roomUser.userId === this.state.user.userId 
                    ? <span style={currentUserTextStyle}>{ roomUser.username } (Score: { roomUser.score })</span>
                    : <span style={buttonTextStyle}>{ roomUser.username } (Score: { roomUser.score })</span>
                  }
                </li>
              );
            })}
          </ul>
        </Row>
        <Row style={centerRowContentStyle}>
          <CopyToClipboard text={joinRoomUrl}>
            <Button>
              <FontAwesomeIcon style={iconStyle} icon={faClipboard} />
              <span style={buttonTextStyle}>Copy link to room to clipboard</span>
            </Button>
          </CopyToClipboard>
        </Row>
      </Grid>
    );
  }
}

const mapStateToProps = (state, properties) => {
  return { room: state.room, user: state.user };
}

const RoomUsers = connect(mapStateToProps)(ConnectedRoomUsers);
export default RoomUsers;