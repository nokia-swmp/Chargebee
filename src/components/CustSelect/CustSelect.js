import React from 'react';
import { SelectItemNew } from '@nokia-csf-uxr/csfWidgets';
import '@nokia-csf-uxr/csfWidgets/csfWidgets.css'


const customers2 = [
  { label: 'Joe', value: 'Joe' },
  { label: 'Sara', value: 'Sara' },
  { label: 'Dave', value: 'Dave' },
  { label: 'Anna', value: 'Anna' },
  { label: 'Julian', value: 'Julian' },
  { label: 'Erica', value: 'Erica' },
];

class CustSelect extends React.Component {
  state = {
    selectedItem: ''
  }
  onChange = (newText) => {
    this.setState({
      selectedItem: newText.value
    });
  }
  render() {
	  return (
		<SelectItemNew
					id="custselect"
					label="Select Customer"
					options={customers2}
					selectedItem={this.state.selectedItem}
					onChange={this.onChange}
                    searchable={true}
                    unCommittedValueErrorMsg = "Customer not found"
                    isRequired
				 />
	  )
	};
}

export default CustSelect