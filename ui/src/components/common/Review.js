import React, { Component } from 'react';
import { Grid, Row, Alert } from 'react-bootstrap';
import FontAwesomeIcon from '@fortawesome/react-fontawesome';
import faUser from '@fortawesome/fontawesome-free-solid/faUser';
import Config from '../../constant/Config';
import { iconStyle, buttonTextStyle, centerRowContentStyle } from "../../constant/Styles";

class Review extends Component {
  constructor(props) {
    super(props);
    this.state = {
      roundId: props.roundId,
      ratings: []
    };
  }

  componentWillMount = async () => {
    const ratingsRes = await fetch(`${Config.apiurl}/ratings?roundId=${this.state.roundId}`);
    if (ratingsRes.status === 200) {
      const ratings = await ratingsRes.json();
      this.setState({ ratings });
    }
  }

  shouldComponentUpdate = (nextProps, nextState) => {
    return this.state.ratings.length !== nextState.ratings.length;
  }

  render = () => {
    const alertStyle = {
      padding: "0.5em",
      display: "inline-block",
      marginBottom: 0
    };

    if (this.state.ratings.length !== 0) {
      return (
        <Grid>
          {this.state.ratings.map((rating) => {

            const ratingContent = rating.imageBase64
              ? <img src={ rating.imageBase64 }></img>
              : <Alert style={alertStyle} bsStyle="info">
                  <span>{ rating.word }</span>
                </Alert>
            return (<div key={ rating.userId }>
                <Row style={centerRowContentStyle}>
                  { ratingContent }
                </Row>
                <Row style={centerRowContentStyle}>
                  <FontAwesomeIcon style={iconStyle} icon={faUser} />
                  <span style={buttonTextStyle}>{ rating.username + ": " + rating.votes + " votes" }</span>
                </Row>
              </div>);
          })}
        </Grid>
        );
    } else {
      return <div>No things were voted for!</div>
    }
  }
}

export default Review;