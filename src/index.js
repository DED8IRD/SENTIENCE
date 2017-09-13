import Inferno from 'inferno';
import Component from 'inferno-component';

class App extends Component {
	constructor(props) {
		super(props);
		this.state = {
			msg: "hello"
		};
	}
	
	render() {
		return (
			<div>
				<h1>Test</h1>
				<h3> {this.state.msg} </h3>
			</div>
		);
	}
}

Inferno.render(
	<App />,
	document.getElementById('root')
);
