import Inferno from 'inferno';
import Component from 'inferno-component';

export default class Shitpost extends Component {
	constructor(props) {
		super(props);
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
					<img src={this.props.shitimg} />
				</div>
			</div>
		);
	}
}