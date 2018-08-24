import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import registerServiceWorker from './registerServiceWorker';
import { Router, Route, hashHistory } from 'react-router'
import About from './modules/About'
import Repos from './modules/Repos'


ReactDOM.render(
    (
      <Router history={hashHistory}>
        <Route path="/" component={App}/>
        <Route path="/repos" component={Repos}/>
        <Route path="/about" component={About}/>
      </Router>
    ),
    document.getElementById('root')
);

registerServiceWorker();
