import React, { Component } from 'react';
import { Grid, Col, Row, Button } from 'react-bootstrap'; 
import FontAwesomeIcon from '@fortawesome/react-fontawesome'
import faUser from '@fortawesome/fontawesome-free-solid/faUser'
import faUsers from '@fortawesome/fontawesome-free-solid/faUsers'
import { connect } from "react-redux";
import Config from '../../constant/Config';
import { iconStyle, buttonTextStyle, centerRowContentStyle, centerTitleContentStyle } from "../../constant/Styles"

class ConnectedRoomUsers extends Component {
  constructor(props) {
    super(props);
    this.state = {
      room: { roomUsers: [] }
    };
  }


  componentWillReceiveProps = (newProps) => {
    this.updateComponentState(newProps);
  }

  componentWillMount = () => {
    this.updateComponentState(this.props);
  }

  updateComponentState(newProps) {
    if (!newProps.room || !newProps.room.roomUsers)
      return;
    this.setState({room: newProps.room});
  }

  render = () => {
    var ulStyle = {
      display: "inline-block"
    };
    return (
      <Grid>
        <Row style={centerTitleContentStyle}>
          <FontAwesomeIcon style={iconStyle} icon={faUsers} />
          <span style={buttonTextStyle}>Users in room:</span>
        </Row>
        <Row style={centerRowContentStyle}>
          <ul className="list-group" style={ulStyle}>
            {this.state.room.roomUsers.map((roomUser) => {
              return (
                <li key={roomUser.userId} className="list-group-item">
                  <FontAwesomeIcon style={iconStyle} icon={faUser} />
                  <span style={buttonTextStyle}>{ roomUser.username }</span>
                </li>
              );
            })}
          </ul>
        </Row>
      </Grid>
    );
  }
}

const mapStateToProps = (state, properties) => {
  return { room: state.room };
}

const RoomUsers = connect(mapStateToProps)(ConnectedRoomUsers);
export default RoomUsers;