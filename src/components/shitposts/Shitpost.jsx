import Inferno from 'inferno';
import Component from 'inferno-component';

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
	'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

export default class Shitpost extends Component {
	constructor(props) {
		super(props);
	}
	
	getTime() {
		var time = this.props.time;
		return MONTHS[time.getMonth()] + " "
			+ time.getDay() + ", " + time.getFullYear()
			+ " at " + time.toLocaleTimeString();
	}
	
	render() {
		return (
			<div className="shitpost">
				<div className="vote">
					<a>▲</a>
					<h3 className="votes">{this.props.votes}</h3>
					<a>▼</a>
				</div>
				<div className="post">
					<h3>{this.props.shitpost}</h3>
					<h4>{this.getTime()}</h4>
					<img src={this.props.shitimg} />
				</div>
			</div>
		);
	}
}