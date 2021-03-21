import React, { Component } from 'react';
import { Grid, Col, Row, Button } from 'react-bootstrap';
import FontAwesomeIcon from '@fortawesome/react-fontawesome'
import faUser from '@fortawesome/fontawesome-free-solid/faUser'
import faUsers from '@fortawesome/fontawesome-free-solid/faUsers'
import faUserSlash from '@fortawesome/fontawesome-free-solid/faUserSlash'
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

  onClickRemoveUser = async (userId) => {
    const removeUserRes = await fetch(`${Config.apiurl}/room/${this.state.room.roomId}/user/${userId}`,
      { method: "DELETE" });
    if (removeUserRes.status === 200) {
      console.log(`Deleted user with id: ${userId}`);
    }
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

    const joinRoomUrl = window.location.host +
      "/?roomCode=" +
      this.state.room.roomCode;

    const buttonStyle = {
      marginLeft: 10
    };

    const isAdminUser = this.state.room.ownerUserId === this.state.user.userId;

    const roomUserListItems = this.state.room.roomUsers.map((roomUser) => {
      const isCurrentUser = roomUser.userId === this.state.user.userId;
      return (
        <li key={roomUser.userId} className="list-group-item">
          <FontAwesomeIcon style={iconStyle} icon={faUser} />
          { isCurrentUser
            ? <span style={currentUserTextStyle}>{ roomUser.username } (Score: { roomUser.score })</span>
            : <span style={buttonTextStyle}>{ roomUser.username } (Score: { roomUser.score })</span>
          }
          { (!isAdminUser && !isCurrentUser) ||
          <Button style={buttonStyle}
                  onClick={(e) => this.onClickRemoveUser(roomUser.userId)}>
            <FontAwesomeIcon style={iconStyle} icon={faUserSlash} />
            <span style={buttonTextStyle}>{ roomUser.userId === this.state.user.userId ? "Leave" : "Remove" }</span>
          </Button> }
        </li>
      );
    });
    return (
      <Grid style={gridStyle}>
        <Row style={centerTitleContentStyle}>
          <FontAwesomeIcon style={iconStyle} icon={faUsers} />
          <span style={buttonTextStyle}>Players in room:</span>
        </Row>
        <Row style={centerRowContentStyle}>
          <ul className="list-group" style={ulStyle}>
            { roomUserListItems }
          </ul>
        </Row>
        <Row style={centerRowContentStyle}>
          <CopyToClipboard text={joinRoomUrl}>
            <Button>
              <FontAwesomeIcon style={iconStyle} icon={faClipboard} />
              <span style={buttonTextStyle}>Copy room link to clipboard</span>
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