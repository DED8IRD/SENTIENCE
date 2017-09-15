import Inferno from 'inferno';
import Component from 'inferno-component';
import ShitpostFeed from './shitposts/ShitpostFeed';

export default class App extends Component {
	constructor(props) {
		super(props);
		this.state = {
			shitposts: []
		};
		for (var i = 0; i < 100; ++i) {
			this.state.shitposts.push({post:"A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C A E S T H E T I C", img:""});
		}
	}
	
	render() {
		return (
			<div>
				<ShitpostFeed
					shitposts={this.state.shitposts} />
			</div>
		);
	}
}