import React, { Component } from 'react';
import { Route, Switch, BrowserRouter, Redirect } from 'react-router-dom';
import { Provider } from 'react-redux'
import Lobby from './components/views/Lobby';
import Room from './components/views/Room';
import store from "./redux/Store";
import { updateUserState, updateRoomState } from "./redux/Actions";
import './App.css';

window.store = store;

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoading: false,
    };
  }

  componentDidMount() {
    const userId = localStorage.getItem("userId");
    if (userId !== null)
      store.dispatch(updateUserState({ "userId": parseInt(userId) }))

    const roomId = localStorage.getItem("roomId");
    if (roomId !== null)
      store.dispatch(updateRoomState({ "roomId": parseInt(roomId) }))
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
