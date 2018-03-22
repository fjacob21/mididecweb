import React , { Component, PropTypes } from 'react'
import { browserHistory} from 'react-router'

class Navbar extends React.Component{
        constructor(props) {
                super(props);
                this.state = {color: "#FF0000"};
        }

        componentDidMount(){
        }

        componentWillUnmount(){
        }

        onCreate(event){
                event.preventDefault();
                //this.context.router.push(this.props.prev)
        }

        onInvite(event){
                event.preventDefault();
                //this.context.router.push("/")
        }

        onMsg(event){
                event.preventDefault();
        }

        onAlert(event){
                event.preventDefault();
        }

        onProfile(event){
                event.preventDefault();
        }

        render(){
                return (
                        <div className='navbar'>
                                <div className='create-link' onClick={this.onCreate.bind(this)}>Create</div>
                                <div className='invite-link' onClick={this.onInvite.bind(this)}>Invite</div>
                                <img className='logo' src='res/drawables/mididec.png' />
                                <div className='msg-icon material-icons' onClick={this.onMsg.bind(this)}>message</div>
                                <div className='alert-icon material-icons' onClick={this.onAlert.bind(this)}>notifications_none</div>
                                <div className='profile-icon material-icons' onClick={this.onMsg.bind(this)}>face</div>
                        </div>)
        }
}

Navbar.contextTypes = {
  router: PropTypes.object.isRequired
};
module.exports = Navbar;
