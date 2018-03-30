import React from 'react';
import ReactDOM from 'react-dom';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';
import App from './App';
import registerServiceWorker from './registerServiceWorker';
import './index.css';


const init = async () => {
  ReactDOM.render(
    <App />,
    document.getElementById('root'),
  );
};

init();
registerServiceWorker();
