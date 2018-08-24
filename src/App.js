import React from 'react';
import MyHead from './components/MyHead/MyHead';
import MyForm from './components/MyForm/MyForm';
//import MyFooter from './components/MyFooter/MyFooter';
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
            </footer>
		</div>
    );
  }
}



export default MySite;
