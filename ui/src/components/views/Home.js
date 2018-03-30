import React, { Component } from 'react';
import logo from '../../logo.svg';
import './Home.css';

class Home extends Component {
  render() {
    return (
      <div className="home">
        <header className="home-header">
          <img src={logo} className="home-logo" alt="logo" />
          <h1 className="home-title">React Template</h1>
        </header>
        <p className="home-intro">
          To get started, edit <code>src/Home.js</code> and save to reload.
        </p>
      </div>
    );
  }
}

export default Home;
