import Inferno from 'inferno';
import Component from 'inferno-component';

export default class Navbar extends Component {
	constructor(props) {
		super(props);
	}
	
	render() {
		return (
			<div className="navbar">
				<h1 className="nav-title"> SENTIENCE </h1>
			</div>
		);
	}
}