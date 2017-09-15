import Inferno from 'inferno';
import Component from 'inferno-component';

export default class Post extends Component {
	constructor(props) {
		super(props);
	}
	
	render() {
		return (
			<div>
				<h3>{this.props.shitpost}</h3>
			</div>
		);
	}
}