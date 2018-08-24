import React from 'react';
import PropTypes from 'prop-types';
import logo from './logo.svg'
import { Link } from 'react-router'
import MyHead from './components/MyHead/MyHead';
import MyForm from './components/MyForm/MyForm';
import './App.css';



class MySite extends React.Component {

  render() {
    return (
		<div id="container">
		  <MyHead/>
		  <MyForm/>
		  <footer>
			&copy 2018 Nokia. All rights reserved. Cookies Privacy Terms
			<br/><strong>React: {React.version}</strong>
			<Link to="/about">  About</Link><Link to="/repos">  Repos</Link>
		  </footer>
		</div>
    );
  }
}



export default MySite;
