import Inferno from 'inferno';
import Component from 'inferno-component';

export default class App extends Component {
	constructor(props) {
		super(props);
		this.state = {
			msg: "hello"
		};
	}
	
	render() {
		return (
			<div>
				<h1> TEST </h1>
			</div>
		);
	}
}