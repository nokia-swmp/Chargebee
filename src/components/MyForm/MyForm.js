import React from 'react';
import PropTypes from 'prop-types';
import { SelectItemNew, CalendarNew, TextArea, Label, TextInput, Button } from '@nokia-csf-uxr/csfWidgets';
import '@nokia-csf-uxr/csfWidgets/csfWidgets.css'
import './MyForm.css';


{/* ---------- FORM HEADER ----------------*/}

const FormHeader = 	<div id="formHeader">
						<p id="blueFormHeader" class="textStyle3">Add a New User</p>
						<p id="greyFormHeader" class="textStyle4">Please add new user activity to existing subscriptions</p>
					</div>

{/* ---------- TEST CUTSTOMERS ----------------*/}

const customers = [
  { label: 'Joe', value: 'Joe' },
  { label: 'Sara', value: 'Sara' },
  { label: 'Dave', value: 'Dave' },
  { label: 'Anna', value: 'Anna' },
  { label: 'Julian', value: 'Julian' },
  { label: 'Erica', value: 'Erica' },
];

{/* ---------- TEST SUBS ----------------*/}

const subscriptions = [
  { label: 'Sub1', value: 'Sub1' },
  { label: 'Sub2', value: 'Sub2' },
  { label: 'Sub12', value: 'Sub12' },
  { label: 'BlablaSub', value: 'BlablaSub' },
  { label: 'Nokia-demos', value: 'Nokia-demos' },
  { label: 'SuperGoodStuff', value: 'SuperGoodStuff' },
];


{/* ---------- DEFAULT DESC TEXT ----------------*/}
const description_text = '';

{/* ---------- MAIN MYFORM CLASS ----------------*/}
class MyForm extends React.Component {

    /* -------------- STATE -----------------*/

    state = {
        selectedCust: '',
        selectedSub: '',
        desc: description_text,
        charCount: description_text.length,
        amount: '',
        amountError: false,
        descLengthError: false,
        dateError: false,
    }

    /* -------------- CONTROLLERS -----------------*/

    onDescChange = (newDesc) => {
        this.setState({
            desc: newDesc.value,
            charCount: newDesc.value.length,
            descLengthError: newDesc.value.length > 150,
        });
    }

    onCustChange = (newText) => {  this.setState({selectedCust: newText.value}); }
	
    onSubChange = (newSub)  => {  this.setState({selectedSub: newSub.value });	}
  
    onAmountChange = (newAmount) => { this.setState({ amount: newAmount.value });  }

    /* onButtonClick = */

    /*--------------- VALIDATION --------------*/

    CheckIfAmountIsValid = (newAmount) => {
        var am = Number(newAmount.value);
        if ( isNaN(am) || am < 0 )
            {this.setState({ amountError: true});}
        else
            {this.setState({ amountError: false});}
    }

    /* -------------- RENDER -----------------*/

    render() {
	  return (
		<div id="MyForm">
			{FormHeader}
			<SelectItemNew
				id="CustSelect"
				label="Customer Name"
				options={customers}
				selectedItem={this.state.selectedCust}
				onChange={this.onCustChange}
				searchable={true}
				unCommittedValueErrorMsg = "Customer not found"
				isRequired
			 />
			<SelectItemNew
				id="SubSelect"
				label="Subscription ID"
				options={subscriptions}
				selectedItem={this.state.selectedSub}
				onChange={this.onSubChange}
				searchable={true}
				isRequired
			/>
			<TextInput
				id="amount"
				placeholder="Add amount"
				label="Amount ($ per hour)"
				focus
				text={this.state.amount}
				onChange={this.onAmountChange}
				onBlur = {this.CheckIfAmountIsValid}
				error = {this.state.amountError}
				errorMsg = "Invalid amount"
				required
			/>
			<div id="DescDiv">
                <Label id="DescLabel" text="Description" />
                <TextArea
                   id="Desc"
                   lockWidth
                   lockHeight
                   text={this.state.desc}
                   onChange={this.onDescChange}
                   error={this.state.descLengthError}
                   errorMsg="Too much text"
                   charCount={this.state.charCount}
                   maxCharCount={150}
                />
			</div>
			<div id="SubmitButton" align="right">
                <Button
                   id="Submit"
                   text="Submit"
                   iconPosition='right'
                   onClick={this.onButtonClick}
                   isCallToAction
                />
			</div>
			<div id="footerContainer"></div>
		</div>
	  )
	};
}

export default MyForm;