
// NINCS KOZE A TOBBIHOZ

import React from 'react';
import PropTypes from 'prop-types';
import { SelectItemNew } from '@nokia-csf-uxr/csfWidgets';
import '@nokia-csf-uxr/csfWidgets/csfWidgets.css'


const customers = [
  { label: 'Joe', value: 'Joe' },
  { label: 'Sara', value: 'Sara' },
  { label: 'Dave', value: 'Dave' },
  { label: 'Anna', value: 'Anna' },
  { label: 'Julian', value: 'Julian' },
  { label: 'Erica', value: 'Erica' },
];

class CustSelect extends React.Component {
  state = {
    selectedItem: 'Joe'
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
					options={customers}
					selectedItem={this.state.selectedItem}
					onChange={this.onChange}
				 />
	  )
	};
}

export default CustSelect