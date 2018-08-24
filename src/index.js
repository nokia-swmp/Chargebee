import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import registerServiceWorker from './registerServiceWorker';
import { Router, Route, hashHistory } from 'react-router'
import Results from './modules/Results'


ReactDOM.render(
    (
      <Router history={hashHistory}>
        <Route path="/" component={App}/>
        <Route path="/results" component={Results}/>
      </Router>
    ),
    document.getElementById('root')
);

registerServiceWorker();
