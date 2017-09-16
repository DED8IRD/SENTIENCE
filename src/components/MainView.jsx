import Inferno from 'inferno';
import Component from 'inferno-component';
import Navbar from './navigation/Navbar';
import ShitpostFeed from './shitposts/ShitpostFeed';

export default class MainView extends Component {
	constructor(props) {
		super(props);
		this.state = {
			shitposts: []
		};
		for (var i = 0; i < 100; ++i) {
			this.state.shitposts.push({post:"A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C", img:"https://i.imgur.com/lTO9Plf.png"});
		}
	}
	
	render() {
		return (
			<div>
				<ShitpostFeed
					shitposts={this.state.shitposts} />
				<Navbar />
			</div>
		);
	}
}