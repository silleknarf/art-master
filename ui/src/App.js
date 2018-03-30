import React, { Component } from 'react';
import { Route, Switch, BrowserRouter, Redirect } from 'react-router-dom';
import Home from './components/views/Home';
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
          <Switch>
            <Route path="/" component={Home} />
          </Switch>
        </Switch>
      </BrowserRouter>
    );
  }
}

export default App;
