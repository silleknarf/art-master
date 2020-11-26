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
import { handleRequest } from "../../utils";

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

  updateUserIdByRoomId = (userId, roomId) => {
    const originalUserIdByRoomIdJson = localStorage.getItem("userIdByRoomId")
    const userIdByRoomId = originalUserIdByRoomIdJson ? JSON.parse(originalUserIdByRoomIdJson) : {};
    userIdByRoomId[roomId] = userId;
    const userIdByRoomIdJson = JSON.stringify(userIdByRoomId);
    localStorage.setItem("userIdByRoomId", userIdByRoomIdJson);
  };

  createUser = async (username, roomId) => {
    const url = `${Config.apiurl}/user/${username}`;
    const user = await handleRequest("POST", url, "Unable to create username");
    this.updateUserIdByRoomId(user.userId, roomId)
    store.dispatch(updateUserState(user));
    return user;
  }

  onCreateRoom = async (username) => {
    const url = `${Config.apiurl}/room`;
    const { roomId, roomCode } = await handleRequest("POST", url, "Unable to create room");
    const { userId } = await this.createUser(username, roomId);
    const joinRoomUrl = `${Config.apiurl}/room/${roomId}/user/${userId}`;
    await handleRequest("POST", joinRoomUrl, "Unable to join room");
    localStorage.setItem("roomId", roomId);
    store.dispatch(updateRoomState({ roomId: roomId }));
    const socket = io(Config.apiurl);
    socket.emit("join", roomId);
    this.props.history.push(`/room/${roomCode}`);
  }

  onJoinRoom = async (roomCode, username) => {
    const getRoomUrl = `${Config.apiurl}/room?roomCode=${roomCode}`;
    const { roomId } = await handleRequest("GET", getRoomUrl, "Unable to get room to join");
    const isUsernameAlreadyInRoom = room.roomUsers.map(ru => ru.username).includes(username);
    if (isUsernameAlreadyInRoom) {
      throw new Error(`The username ${username} has already been taken`);
    }
    const { userId } = await this.createUser(username, roomId);
    const joinRoomUrl = `${Config.apiurl}/room/${roomId}/user/${userId}`;
    await handleRequest("POST", joinRoomUrl, "Unable to join room");
    localStorage.setItem("roomId", roomId);
    store.dispatch(updateRoomState({ roomId: roomId }));
    this.props.history.push(`/room/${roomCode}`);
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
                onClick={handleSubmit} 
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
                onClick={handleSubmit} 
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