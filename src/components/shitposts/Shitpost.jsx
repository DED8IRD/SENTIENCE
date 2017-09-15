import Inferno from 'inferno';
import Component from 'inferno-component';

export default class Post extends Component {
	constructor(props) {
		super(props);
	}
	
	render() {
		return (
			<div className="shitpost">
				<h3>{this.props.shitpost}</h3>
			</div>
		);
	}
}