import Inferno from 'inferno';
import Component from 'inferno-component';
import ShitpostModal from './ShitpostModal';

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
	'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

export default class Shitpost extends Component {
	constructor(props) {
		super(props);
		
		this.showShitpostModal = this.showShitpostModal.bind(this);
	}
	
	getTime() {
		var time = this.props.time;
		return MONTHS[time.getMonth()] + " "
			+ time.getDay() + ", " + time.getFullYear()
			+ " at " + time.toLocaleTimeString();
	}
	
	showShitpostModal(e) {
		this.props.modal(
			<ShitpostModal
					id={this.props.id}
					name={this.props.name}
					votes={this.props.votes}
					time={this.props.time}
					shitpost={this.props.post}
					shitimg={this.props.img}
					modal={this.props.modal} />
		);
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
					<h3 onClick={this.showShitpostModal}>
						{this.props.shitpost}
					</h3>
					<h4 onClick={this.showShitpostModal}>
						{this.getTime()}
					</h4>
					<img src={this.props.shitimg}
						onClick={this.showShitpostModal} />
				</div>
			</div>
		);
	}
}