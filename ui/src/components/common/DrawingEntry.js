import React, { Component } from 'react';
import Config from '../../constant/Config';

class DrawingEntry extends Component {
  constructor(props) {
    super(props);
    this.state = {
      entry: {
        key: "Word"
      }
    };
  }

  componentDidMount = () => {
    this.updateEntry(this.props.entryId);
  }

  updateEntry = async (entryId) => {
    if (!entryId) return;
    var entryRes = await fetch(`${Config.apiurl}/entry?entryId=${entryId}`);
    if (entryRes.status === 200) {
      const entry = await entryRes.json();
      this.setState({entry: entry});
    }
  }

  render = () => {
    const style = {
      margin: "10px",
      fontSize: "medium"
    };
    const rowStyle = {
      textAlign: "center"
    };
    return (
      <div style={rowStyle}>
        <div style={style}>
          🎨 Artists, it's time to draw! You have to draw <strong>{ JSON.stringify(this.state.entry) }</strong>
        </div>
      </div>
    );
  }
}

export default DrawingEntry;