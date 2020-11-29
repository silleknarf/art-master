import React, { Component } from "react";
import { Button } from "react-bootstrap";
import FontAwesomeIcon from "@fortawesome/react-fontawesome";
import faEnvelope from "@fortawesome/fontawesome-free-solid/faEnvelope";
import { iconStyle } from "../../constant/Styles";

class Feedback extends Component 
{
  render() {
    const feedbackButtonStyle = {
      color: "black",
      backgroundColor: "white",
      margin: "10px",
      display: "inline-block",
      width: "initial"
    };
    const buttonHolderStyle = {
      width: "100%"
    };
    return (
      <div style={buttonHolderStyle}>
        <Button
          className="button"
          style={feedbackButtonStyle}
          href="mailto:support@craicbox.app?subject=Craicbox - Feedback"
          type="submit">
          <FontAwesomeIcon style={iconStyle} icon={faEnvelope} />
          Feedback
        </Button>
      </div>
    );
  }
}

export default Feedback;