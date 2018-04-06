import React , { Component, PropTypes } from 'react'
import { browserHistory} from 'react-router'
import createHistory from "history/createHashHistory"

const history = createHistory();
class Navbar extends React.Component{
        constructor(props) {
                super(props);
                this.state = {color: "#FF0000"};
                this.onHome = this.onHome.bind(this);
                this.onMailingList = this.onMailingList.bind(this);
        }

        componentDidMount(){
        }

        componentWillUnmount(){
        }

        onHome(event){
                event.preventDefault();
                history.replace("/");
        }

        onMailingList(event){
                event.preventDefault();
                history.replace("/mailinglist");
        }

        render(){
                return (
                        <div className='navbar'>
                                <div id='lhome' className='create-link' onClick={this.onHome}>Home</div>
                                <img id='lhomeicon' className='logo' src='res/drawables/mididec.png' onClick={this.onHome}/>
                                <div id='lmailinglist' className='create-link' onClick={this.onMailingList}>Mailing List</div>
                        </div>)
        }
}

module.exports = Navbar;
