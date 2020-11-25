import React, { Component } from 'react';
import { Grid, Row, Button, Form, FormControl, FormGroup, HelpBlock, ControlLabel, Tabs, Tab } from 'react-bootstrap';
import io from "socket.io-client";
import { Formik } from 'formik';
import * as yup from 'yup';
import Config from '../../constant/Config';
import store from '../../redux/Store';
import { updateRoomState, updateUserState } from "../../redux/Actions";
import './Lobby.css';
import { centerTitleContentStyle, centerRowContentStyle, tabsStyle, titleStyle } from "../../constant/Styles"

class Lobby extends Component {

  createRoomSchema = yup.object({
    username: yup.string().required()
  });

  joinRoomSchema = yup.object({
    roomCode: yup.string().length(4, "Must be exactly 4 letters").required(),
    username: yup.string().required()
  });

  gridStyle = {
    padding: "2em"
  };

  constructor(props) {
    super(props);
    this.state = {
      roomCode: "",
      tabIndex: 1
    }
  }

  /**
   * Calls an API endpoint, handling errors
   * - Converts non-200 statuses into errors
   * - Adds context to errors
   */
  handleRequest = async (method, url, failureMessage) => {
    try {
      console.log(`${method} ${url}`);
      const res = await fetch(url, {
        method: method,
      });

      var resBody = await res.json();

      if (res.status !== 200) {
        const errorText = resBody.message || resBody.error || "Error Unknown";
        const error = new Error(`${errorText} (Error: ${res.status})`);
        throw error;
      }
      return resBody;

    } catch (err) {
      const error = new Error(`${failureMessage}. ${err.message}`);
      throw error;
    }
  }

  createUser = async (username, roomId) => {
    const url = `${Config.apiurl}/user/${username}`;
    const user = await this.handleRequest("POST", url, "Unable to create username");
    localStorage.setItem("userId", user.userId);
    store.dispatch(updateUserState(user));
    return user;
  }

  onCreateRoom = async (username) => {
    const { userId } = await this.createUser(username);
    const url = `${Config.apiurl}/room?userId=${userId}`;
    const room = await this.handleRequest("POST", url, "Unable to create room");
    localStorage.setItem("roomId", room.roomId);
    store.dispatch(updateRoomState({ roomId: room.roomId }));
    const socket = io(Config.apiurl);
    socket.emit("join", room.roomId);
    this.props.history.push(`/room/${room.roomCode}`);
  }

  onJoinRoom = async (roomCode, username) => {
    const getRoomUrl = `${Config.apiurl}/room?roomCode=${roomCode}`;
    const room = await this.handleRequest("GET", getRoomUrl, "Unable to get room to join");
    const isUsernameAlreadyInRoom = room.roomUsers.map(ru => ru.username).includes(username);
    if (isUsernameAlreadyInRoom) {
      throw new Error(`The username ${username} has already been taken`);
    }
    const { userId } = await this.createUser(username);
    const joinRoomUrl = `${Config.apiurl}/room/${room.roomId}/user/${userId}`;
    await this.handleRequest("POST", joinRoomUrl, "Unable to join room");
    localStorage.setItem("roomId", room.roomId);
    store.dispatch(updateRoomState({ roomId: room.roomId }));
    this.props.history.push(`/room/${roomCode}`);
  }

  onKeyDown = (event: React.KeyboardEvent<HTMLDivElement>) => {
    // 'keypress' event misbehaves on mobile so we track 'Enter' key via 'keydown' event
    if (event.key === "Enter") {
      event.preventDefault();
      event.stopPropagation();
      if (this.state.tabIndex === 1)
        this.onCreateRoom(event);
      else
        this.onJoinRoom(event);
    }
  }

  handleSelect = (key) => {
    this.setState({ tabIndex: key });
  }

  componentDidMount = () => {
    const roomCode = this.getUrlParam("roomCode");
    if (roomCode)
      this.setState({
        tabIndex: 2,
        roomCode: roomCode
      });
  }

  getUrlParam = (name) => {
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results)
      return results[1] || "";
    return "";
  }

  getUsernameRow = (values, handleChange, touched, errors) => (
    <div>
      <Row style={centerRowContentStyle} className="input-row">
        <ControlLabel className="label">Username</ControlLabel>
      </Row>
      <Row style={centerRowContentStyle} className="input-row">
        <FormGroup>
          <FormControl
            className="username-input"
            name="username"
            type="text"
            value={values.username}
            onChange={handleChange}
            onKeyDown={this.onKeyDown}
          />
        </FormGroup>
        {errors.username && <HelpBlock>{errors.username}</HelpBlock>}
      </Row>
    </div>
  );

  getCreateRoomForm = () => (
    <Formik
      validationSchema={this.createRoomSchema}
      onSubmit={(values, actions) => {
        this.onCreateRoom(values.username)
          .catch(error => {
            actions.setFieldError("general", error.message);
          });
      }}
      initialValues={{
        username: ""
      }}>
      {({
        handleSubmit,
        handleChange,
        handleBlur,
        values,
        touched,
        isValid,
        errors
      }) =>
        (<Form noValidate onSubmit={handleSubmit}>
          <Grid style={this.gridStyle}>
            {this.getUsernameRow(values, handleChange, touched, errors)}
            <Row style={centerRowContentStyle} className="input-row">
              <Button
                className="create-room-button button"
                type="submit">
                Create Room
            </Button>
              {errors.general && <HelpBlock>{errors.general}</HelpBlock>}
            </Row>
          </Grid>
        </Form>)}
    </Formik>
  );

  getJoinRoomForm = () => (
    <Formik
      validationSchema={this.joinRoomSchema}
      onSubmit={(values, actions) => {
        this.onJoinRoom(values.roomCode, values.username)
          .catch(error => {
            actions.setFieldError("general", error.message);
          });
      }}
      enableReinitialize
      initialValues={{
        username: "",
        roomCode: this.state.roomCode
      }}>
      {({
        handleSubmit,
        handleChange,
        handleBlur,
        values,
        touched,
        isValid,
        errors
      }) =>
        (<Form noValidate onSubmit={handleSubmit}>
          <Grid style={this.gridStyle}>
            <Row style={centerRowContentStyle} className="input-row">
              <ControlLabel className="label">Room Code</ControlLabel>
            </Row>
            <Row style={centerRowContentStyle} className="input-row">
              <FormGroup>
                <FormControl
                  className="room-code-input"
                  type="text"
                  name="roomCode"
                  onChange={handleChange}
                  value={values.roomCode}
                  onKeyDown={this.onKeyDown}
                />
              </FormGroup>
              {touched.roomCode && errors.roomCode && <HelpBlock>{errors.roomCode}</HelpBlock>}
            </Row>
            {this.getUsernameRow(values, handleChange, touched, errors)}
            <Row style={centerRowContentStyle} className="button-row">
              <Button
                className="join-room-button button"
                type="submit">
                Join Room
            </Button>
              {errors.general && <HelpBlock>{errors.general}</HelpBlock>}
            </Row>
          </Grid>
        </Form>)}
    </Formik>
  );

  render() {
    return (
      <div className="lobby">
        <div style={centerTitleContentStyle}>
          <span style={titleStyle}>Craicbox</span>
        </div>
        <Tabs
          id="lobby-tabs"
          activeKey={this.state.tabIndex}
          style={tabsStyle}
          onSelect={this.handleSelect}>
          <Tab eventKey={1} title="Create Room">
            {this.getCreateRoomForm()}
          </Tab>
          <Tab eventKey={2} title="Join Room">
            {this.getJoinRoomForm()}
          </Tab>
        </Tabs>
      </div>
    );
  }
}

export default Lobby;