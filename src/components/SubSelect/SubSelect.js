//NINCS KOZE A TOBBIHOZ

import React from 'react';
import PropTypes from 'prop-types';
import { SelectItemNew } from '@nokia-csf-uxr/csfWidgets';
import '@nokia-csf-uxr/csfWidgets/csfWidgets.css'


const subscriptions = [
  { label: 'Sub1', value: 'Sub1' },
  { label: 'Sub2', value: 'Sub2' },
  { label: 'Sub12', value: 'Sub12' },
  { label: 'BlablaSub', value: 'BlablaSub' },
  { label: 'Nokia-demos', value: 'Nokia-demos' },
  { label: 'SuperGoodStuff', value: 'SuperGoodStuff' },
];

class SubSelect extends React.Component {
  state = {
    selectedItem: 'Sub1'
  }
  onChange = (newText) => {
    this.setState({
      selectedItem: newText.value
    });
  }
  render() {
	  return (
		<SelectItemNew
					id="suselect"
					label="Select Subscription"
					options={subscriptions}
					selectedItem={this.state.selectedItem}
					onChange={this.onChange}
				 />
	  )
	};
}

export default SubSelect