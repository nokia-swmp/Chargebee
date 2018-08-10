import React from 'react';
import PropTypes from 'prop-types';
import { SelectItemNew, CalendarNew, TextArea, Label, TextInput } from '@nokia-csf-uxr/csfWidgets';
import '@nokia-csf-uxr/csfWidgets/csfWidgets.css'
import './MyForm.css';


const customers = [
  { label: 'Joe', value: 'Joe' },
  { label: 'Sara', value: 'Sara' },
  { label: 'Dave', value: 'Dave' },
  { label: 'Anna', value: 'Anna' },
  { label: 'Julian', value: 'Julian' },
  { label: 'Erica', value: 'Erica' },
];

const subscriptions = [
  { label: 'Sub1', value: 'Sub1' },
  { label: 'Sub2', value: 'Sub2' },
  { label: 'Sub12', value: 'Sub12' },
  { label: 'BlablaSub', value: 'BlablaSub' },
  { label: 'Nokia-demos', value: 'Nokia-demos' },
  { label: 'SuperGoodStuff', value: 'SuperGoodStuff' },
];

const description_text = '';

const FormHeader = 	<div id="formHeader">
						<p id="blueFormHeader" class="textStyle3">Add a New User</p>
						<p id="greyFormHeader" class="textStyle4">Please add new user activity to existing subscriptions</p>
					</div>

class MyForm extends React.Component {
  state = {
    selectedCust: '',
	selectedSub: '',
	desc: description_text,
	charCount: description_text.length,
    error: false,
	amount: '',
  }
  
 onDescChange = (newDesc) => {
    this.setState({
	  desc: newDesc.value,
      charCount: newDesc.value.length,
      error: newDesc.value.length > 150,
    });
  }
  
  onCustChange = (newCust) =>{  this.setState({selectedCust: newCust.value,}); }
	
  onSubChange = (newSub)  => {  this.setState({selectedSub: newSub.value });	}
  
  onAmountChange = (newAmount) => { this.setState({ amount: newAmount.value });  }
	
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
			 />
			 <SelectItemNew
				id="SubSelect"
				label="Subscription ID"
				options={subscriptions}
				selectedItem={this.state.selectedSub}
				onChange={this.onSubChange}
				searchable={true}
			 /> 
			 <TextInput
				text={this.state.amount}
				id="amount"
				placeholder="placeholder"
				label="Amount (per hour)"
				focus
				onChange={this.onAmountChange}
			 />
			 <Label id="DescLabel" text="Description" />
			 <TextArea
				id="Desc"
				text={this.state.desc}
				onChange={this.onDescChange}
				error={this.state.error}
				errorMsg="Too much text"
				charCount={this.state.charCount}
				maxCharCount={150}
			 />
		</div>
	  )
	};
}

export default MyForm;