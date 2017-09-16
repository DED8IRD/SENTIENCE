import Inferno from 'inferno';
import Component from 'inferno-component';

export default class Shitpost extends Component {
	constructor(props) {
		super(props);
	}
	
	render() {
		return (
			<div className="shitpost">
				<h3>{this.props.shitpost}</h3>
				<img src={this.props.shitimg} />
			</div>
		);
	}
}