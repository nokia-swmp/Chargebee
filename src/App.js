import React from 'react';
import PropTypes from 'prop-types';
import logo from './logo.svg'
import MyHead from './components/MyHead/MyHead';
import MyForm from './components/MyForm/MyForm';


class MySite extends React.Component {
 
 

  render() {
    return (
		<div id="maindiv">
		  <MyHead/>
		  <MyForm/>
		  <footer id="MyFooter">
			&copy 2018 Nokia. All rights reserved. Cookies Privacy Terms
		  </footer>
		</div>
    );
  }
}



export default MySite;