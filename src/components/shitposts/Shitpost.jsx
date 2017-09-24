import Inferno from 'inferno';
import Component from 'inferno-component';
import ShitpostModal from './ShitpostModal';

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
	'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

export default class Shitpost extends Component {
	constructor(props) {
		super(props);
		
		this.showShitpostModal = this.showShitpostModal.bind(this);
		this.upvotePost = this.upvotePost.bind(this);
		this.downvotePost = this.downvotePost.bind(this);
	}
	
	getTime() {
		var time = this.props.time;
		return MONTHS[time.getMonth()] + " "
			+ time.getDate() + ", " + time.getFullYear()
			+ " at " + time.toLocaleTimeString();
	}
	
	showShitpostModal(e) {
		this.props.modal(
			<ShitpostModal
					id={this.props.id}
					name={this.props.name}
					votes={this.props.votes}
					time={this.props.time}
					shitpost={this.props.shitpost}
					shitimg={this.props.shitimg}
					modal={this.props.modal} />
		);
	}
	
	upvotePost() {
		// how 2 upvote???!?
	}
	
	downvotePost() {
		// how 2 downvote???!?
	}
	
	render() {
		return (
			<div className="shitpost">
				<div className="vote">
					<a onClick={this.upvotePost}>▲</a>
					<h3 className="votes">{this.props.votes}</h3>
					<a onClick={this.downvotePost}>▼</a>
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