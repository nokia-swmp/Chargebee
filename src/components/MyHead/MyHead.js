import React from 'react';
import './MyHead.css';
import Nokia from './Nokia.svg';



class MyHead extends React.Component {
	
   
  
  render() {
	  return (
		<div>
			<head>
				<title>Add</title>
				<meta charset="utf-8"></meta>
				<meta name="viewport" content="width=device-width, initial-scale=1"></meta>
				//<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
				//<script src="{% static 'js/addLineItem.js' %}"></script>
			</head>
			<header id="whiteHeader">
				<div id="header1">
					<a href="https://networks.nokia.com/"> <img src={Nokia} id="NokiaLogo" alt="Nokia-wordmark"/></a>
					<a href="https://networks.nokia.com/software" id="whiteHeaderSoftwareTitle">Software</a>
					<span id="whiteHeader-tail">All Nokia Sites</span>
				</div>
			</header>
			<header id="blueHeader">
				<div class="textStyle">ChargeBee Data Portal
					<br/><span class="textStyle2" id="blueHeaderSubtitle">Get ChargeBee user data</span>
				</div>
			</header>
		</div>
	  )
  }
  
  
}


export default MyHead;