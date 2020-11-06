import React from 'react';
import ReactDOM from 'react-dom';
import io from "socket.io-client";
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';
import App from './App';
import registerServiceWorker from './registerServiceWorker';
import './index.css';
import Config from "./constant/Config";

const init = async () => {
  ReactDOM.render(
    <App />,
    document.getElementById('root'),
  );
};

init();
registerServiceWorker();

const socket = io(Config.apiurl);
socket.on('connect', function() {
  socket.emit('my event', {data: 'I\'m connected!'});
});

