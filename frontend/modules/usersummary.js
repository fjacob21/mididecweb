import React from 'react'
import createHistory from "history/createHashHistory"
import jquery from 'jquery'
import User from './user'
import { Table, NavLink, Card, CardTitle, CardText, Button } from 'reactstrap';

const history = createHistory();

class UserSummary extends React.Component {
        constructor(props) {
                super(props);
                this.onEdit = this.onEdit.bind(this);
                this.onDelete = this.onDelete.bind(this);
        }

        onEventDetails(event_id, isItem){
            if (!isItem || window.innerWidth < 500)
                history.push("/events/"+event_id);
        }

        onEdit(){
                this.props.onEdit(this.props.user);
        }

        onDelete(){
                this.props.onDelete(this.props.user);
        }

        render(){
                var loguser = User.getSession();
                var lastlogin = new Date(this.props.user.lastlogin).toLocaleString();
                var islogged = this.props.user.loginkey != "";
                var loggedStatus = <i className="material-icons md-light">cloud_off</i>;
                if (islogged)
                        loggedStatus = <i className="material-icons md-light">cloud_queue</i>;
                var btRemove = "";
                if (this.props.user.user_id != loguser.user_id)
                        btRemove = <div className='user-bt' onClick={this.onDelete}><i className="material-icons md-light">delete</i></div>
                return (
                  <div className='user-summary'>
                      <div className='user-name'>{this.props.user.name}</div>
                      <div className='user-email'>{this.props.user.email}</div>
                      <div className='user-lastlogin'>{lastlogin}</div>
                      <div className='user-logged'>{loggedStatus}</div>
                      <div className='user-bt' onClick={this.onEdit}><i className="material-icons md-light">edit</i></div>
                      {btRemove}
                  </div>)
        }
}

module.exports = UserSummary;
