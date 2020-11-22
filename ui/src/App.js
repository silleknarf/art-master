import React, { Component } from "react";
import { Route, Switch, BrowserRouter } from "react-router-dom";
import { Provider } from "react-redux"
import Lobby from "./components/views/Lobby";
import Room from "./components/views/Room";
import store from "./redux/Store";
import "./App.css";

window.store = store;

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
      <Provider store={store}>
        <BrowserRouter>
          <Switch>
            <Route exact path="/" component={Lobby} />
            <Route path="/room" component={Room} />
          </Switch>
        </BrowserRouter>
      </Provider>
    );
  }
}

export default App;
