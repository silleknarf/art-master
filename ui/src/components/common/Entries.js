import React, { Component } from 'react';
import { Grid, Row, Button, FormControl, FormGroup } from 'react-bootstrap';
import FontAwesomeIcon from '@fortawesome/react-fontawesome'
import faPlus from '@fortawesome/fontawesome-free-solid/faPlus'
import faTrash from '@fortawesome/fontawesome-free-solid/faTrash'
import faQuoteLeft from '@fortawesome/fontawesome-free-solid/faQuoteLeft'
import { connect } from "react-redux";
import Config from '../../constant/Config';
import $ from "jquery";
import { iconStyle, buttonTextStyle, centerRowContentStyle, centerTitleContentStyle } from "../../constant/Styles"

class ConnectedEntries extends Component {
  constructor(props) {
    super(props);
    this.state = {
      entries: [],
      user: null,
      room: null,
      newEntry: "",
      minigame: {
        description: [],
        canSeeOwnEntriesOnly: false,
        entryComponents: [""]
      }
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

    const minigame = newProps.minigames && 
      newProps.minigames.length > 0 &&
      newProps.minigames.filter(m => m.minigameId === newProps.room.minigameId)[0];
    if (minigame) this.setState({ minigame });
    this.setState({
      entries: newProps.entries,
      user: newProps.user,
      room: newProps.room,
    });
  }

  onAddEntry = async (e) => {
    const entry = {
      roomId: this.state.room.roomId,
      userId: this.state.user.userId
    };
    const entryComponents = [{ 
      key: this.state.minigame.entryComponents[0],
      value: this.state.newEntry
    }];
    this.setState({newEntry: ""});
    const addEntryRes = await fetch(
      `${Config.apiurl}/entry?${$.param(entry)}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(entryComponents)

      });
    if (addEntryRes.status === 200) {
      console.log(`Added entry: ${JSON.stringify(entry)} with entry components: ${JSON.stringify(entryComponents)}`);
    }
  }

  onClickRemoveEntry = async (entryId) => {
    var entry = { entryId };
    const removeEntryRes = await fetch(`${Config.apiurl}/entry?${$.param(entry)}`,
      { method: "DELETE" });
    if (removeEntryRes.status === 200) {
      console.log(`Deleted entry with id: ${entryId}`);
    }
  }

  onKeyDown = (event: React.KeyboardEvent<HTMLDivElement>) => {
    // 'keypress' event misbehaves on mobile so we track 'Enter' key via 'keydown' event
    if (event.key === 'Enter') {
      event.preventDefault();
      event.stopPropagation();
      this.onAddEntry(event);
    }
  }

  render = () => {
    var ulStyle = {
      display: "inline-block"
    };
    const entryStyle = {
      margin: "10px"
    }
    var buttonStyle = {
      display: "inline-block",
      height: "34px",
      marginTop: "-3px"
    }
    var gridStyle = {
      width: "initial"
    };
    const subtitleTextStyle = {
      ...buttonTextStyle,
      fontSize: "small",
      fontStyle: "italic"
    }

    const titleRow = (<Row style={centerTitleContentStyle}>
        <FontAwesomeIcon style={iconStyle} icon={faQuoteLeft} />
        <span style={buttonTextStyle}>Entries:</span>
          { this.state.minigame.description &&  
            this.state.minigame.description.map(descriptionLine => 
              <div key={descriptionLine} style={subtitleTextStyle}>{ descriptionLine }</div>
            )
          }
      </Row>);

    const ownEntries = this.state.room && this.state.minigame.canSeeOwnEntriesOnly;
    const entryFilter = (entry) =>
      (!ownEntries || entry.userId === this.state.user.userId) &&
      !entry.roundId;

    return (
      <Grid style={gridStyle}>
        { titleRow }
        <Row style={centerRowContentStyle}>
          <ul className="list-group" style={ulStyle}>
            { this.state.entries.filter(entryFilter).map((entry) => {
              return (
                <li key={entry.entryId} className="list-group-item">
                  <span style={entryStyle}>{ entry.entryComponents[0].value }</span>
                  <Button
                    className="btn btn-xs"
                    onClick={(e) => this.onClickRemoveEntry(entry.entryId)}>
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
              type="input"
              placeholder={this.state.minigame.entryComponents[0]}
              onChange={e => this.setState({ newEntry: e.target.value })}
              value={this.state.newEntry}
              onKeyDown={this.onKeyDown}
            />
          </FormGroup>
          <Button
            className="btn"
            onClick={(e) => this.onAddEntry(e)}
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
  return { entries: state.entries, user: state.user, room: state.room, minigames: state.minigames };
}

const Entries = connect(mapStateToProps)(ConnectedEntries);

export default Entries;