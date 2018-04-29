import React, { Component } from 'react';
import { Grid, Col, Row, Button } from 'react-bootstrap'; 
import { connect } from "react-redux";
import Config from '../../constant/Config';

class ConnectedRoomUsers extends Component {
  constructor(props) {
    super(props);
    this.state = {
      room: { roomUsers: [] }
    };
  }

  componentWillReceiveProps = (newProps) => {
    if (!newProps.room.roomUsers)
      return;
    this.setState({room: newProps.room});
  }

  render = () => {
    return (
      <div>
        <div>Users:</div>
        <ul className="list-group">
          {this.state.room.roomUsers.map((roomUser) => {
            return <li key={roomUser.userId} className="list-group-item">{ roomUser.username }</li>;
          })}
        </ul>
      </div>
    );
  }
}

const mapStateToProps = (state, properties) => {
  return { room: state.room };
}

const RoomUsers = connect(mapStateToProps)(ConnectedRoomUsers);
export default RoomUsers;