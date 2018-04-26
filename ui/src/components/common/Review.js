import React, { Component } from 'react';
import { Grid, Col, Row, Button } from 'react-bootstrap'; 
import { connect } from "react-redux";
import Config from '../../constant/Config';

class Review extends Component {
    constructor(props) {
        super(props);
        this.state = {
        	   roundId: props.roundId,
        	   winningImage: null
        };
    }
    
    componentWillMount = async () => {
        const winningImageRes = await fetch(`${Config.apiurl}/ratings?roundId=${this.state.roundId}`);
        if (winningImageRes.status === 200) {
        	    this.state.winningImage = await winningImageRes.json();
        }
    }
    
    render = () => {
        return (
            <div>
            { this.state.winningImage && 
                (<div>
                    <Row>
                        <img src={ "/data/" + this.state.winningImage.winningImageLocation }></img>
                    </Row>
                    <Row>
                        <div>{ this.state.winningImage.winnerUsername }</div>
                    </Row>
                </div>)
            }
            </div>
        );
    }
}

export default Review;