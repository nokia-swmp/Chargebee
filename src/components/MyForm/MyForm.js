import React from 'react';
import { SelectItemNew, CalendarNew, TextArea, Label, TextInput, Button } from '@nokia-csf-uxr/csfWidgets';
import { Link, withRouter } from 'react-router';
import '@nokia-csf-uxr/csfWidgets/csfWidgets.css';
import './MyForm.css';
import CustSelect from '../CustSelect/CustSelect';




/* ---------- FORM HTML ELEMENTS ----------------*/

const FormHeader = 	<div id="formHeader">
						<p id="blueFormHeader" class="textStyle3">Add a New User</p>
						<p id="greyFormHeader" class="textStyle4">Please add new user activity to existing subscriptions</p>
					</div>

var ErrorElement =  <ul id="ErrorMessageList">
                 <li id="AmountErr" class="errors">Invalid amount!</li>
                 <li id="DescriptionErr" class="errors">Description too long!</li>
                 <li id="DateErr" class="errors">Invalid date!</li>
            </ul>


/* ---------- TEST CUTSTOMERS ----------------*/

const customers = [
  { label: 'Joe', value: 'Joe'},
  { label: 'Sara', value: 'Sara' },
  { label: 'Dave', value: 'Dave' },
  { label: 'Anna', value: 'Anna' },
  { label: 'Julian', value: 'Julian' },
  { label: 'Erica', value: 'Erica' },
];

/* ---------- TEST SUBS ----------------*/

const subscriptions = [
  { label: 'Sub1', value: 'Sub1' },
  { label: 'Sub2', value: 'Sub2' },
  { label: 'Sub12', value: 'Sub12' },
  { label: 'BlablaSub', value: 'BlablaSub' },
  { label: 'Nokia-demos', value: 'Nokia-demos' },
  { label: 'SuperGoodStuff', value: 'SuperGoodStuff' },
];


/* ---------- DEFAULT TEXTS ----------------*/
const initial_costumer = '';
const initial_subscription = '';
const initial_amount = '';
const initial_description_text = '';

/* ---------- MAIN MYFORM CLASS ----------------*/
class MyForm extends React.Component {

constructor(props) {
    super(props)
  }

    /* -------------- STATE -----------------*/

    state = {
        selectedCust: initial_costumer,
        selectedSub: initial_subscription,
        desc: initial_description_text,
        charCount: initial_description_text.length,
        amount: initial_amount,
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


    /*--------------- VALIDATION --------------*/

    CheckIfAmountIsValid = (newAmount) => {
        var am = Number(newAmount.value);
        if ( isNaN(am) || am < 0 )
            {this.setState({ amountError: true});}
        else
            {this.setState({ amountError: false});}
    }

    onButtonClick = () => {
        if (this.state.amount == initial_amount)
        {
            this.setState({amountError: true});
            this.state.amountError = true;}
        /* TODO: more emty checks like above */
        if (this.state.amountError || this.state.descLengthError || this.state.dateError)
        {
            if (this.state.amountError) {
                document.getElementById("AmountErr").style.display = "list-item"; }
            if (this.state.descLengthError) {
                document.getElementById("DescriptionErr").style.display = "list-item"; }
            /*TODO: handle all errors */}
        else {
            var Errors = document.getElementsByClassName("errors");
            var i;
            for (i = 0; i < Errors.length; i++)
                Errors[i].style.display = "none";
            alert("Item succesfully added!");
            this.props.router.push('/results');}
    }


    /* -------------- RENDER -----------------*/

    render() {
	  return (
		<div id="MyForm">
			{FormHeader}
			<div id="CustSelectDiv">
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
			</div>
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
			{ErrorElement}
			<div id="SubmitButton" align="right">
                <Button
                   id="Submit"
                   text="Submit"
                   iconPosition='right'
                   onClick={this.onButtonClick}
                   isCallToAction
                />
			</div>
			<Link to="/results">  Results</Link>
			<div id="footerContainer"></div>
		</div>
	  )
	};
}

export default withRouter(MyForm);


/*
TODO: SelectItem doesnt work (SelectedItem prop fail, Selecting with keyboard fail)
TODO: Usage range Calendar can't be found in @nokia-csf library
TODO: SelectedItem crashes with initial value other than ''
*/