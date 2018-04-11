import React, { Component } from 'react';
import { Route, Switch, BrowserRouter, Redirect } from 'react-router-dom';
import Home from './components/views/Home';
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
          <Route exact path="/" component={Home} />
          <Route path="/room" component={Room} />
        </Switch>
      </BrowserRouter>
    );
  }
}

export default App;
