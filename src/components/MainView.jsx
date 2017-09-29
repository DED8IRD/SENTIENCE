import Inferno from 'inferno';
import Component from 'inferno-component';
import Navbar from './navigation/Navbar';
import ShitpostFeed from './shitposts/ShitpostFeed';

export default class MainView extends Component {
	constructor(props) {
		super(props);
		this.state = {
			shitposts: [],
			modal: ''
		};
		for (var i = 0; i < 100; ++i) {
			this.state.shitposts.push({post:"A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C", img:"https://i.imgur.com/lTO9Plf.png", time: new Date(), id: "0", name: "WildWavyShinji", votes: 0});
		}
		
		
		this.setModal = this.setModal.bind(this);
	}
	
	setModal(modal) {
		this.setState({
			modal: modal
		});
	}
	
	render() {
		return (
			<div>
				<ShitpostFeed
					shitposts={this.state.shitposts}
					modal={this.setModal} />
				<Navbar />
				{this.state.modal}
			</div>
		);
	}
}