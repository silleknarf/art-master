import React, { Component } from 'react';
import Config from '../../constant/Config';

class DrawingEntry extends Component {
  constructor(props) {
    super(props);
    this.state = {
      entry: {
        entryComponents: [{
          key: "Word",
          value: ""
        }]
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
    const entryKey = this.state.entry.entryComponents[0].key;
    const entryValue = this.state.entry.entryComponents[0].value;
    return (
      <div style={rowStyle}>
        <div style={style}>
          🎨 Artists, it's time to draw! 
          You have to draw the { entryKey.toLowerCase() }: <strong>{ entryValue }</strong>
        </div>
      </div>
    );
  }
}

export default DrawingEntry;