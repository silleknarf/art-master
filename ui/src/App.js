import React, { Component } from 'react';
import { Route, Switch, BrowserRouter, Redirect } from 'react-router-dom';
import Lobby from './components/views/Lobby';
import Room from './components/views/Room';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoading: false,
    };
  }

  render() {
    if (this.state.isLoading) {
      return (
        <div className="loading-screen">
          <div className="loading-text">Loading...</div>
        </div>
      );
    }
    return (
      <BrowserRouter>
        <Switch>
          <Route exact path="/" component={Lobby} />
          <Route path="/room" component={Room} />
        </Switch>
      </BrowserRouter>
    );
  }
}

export default App;
