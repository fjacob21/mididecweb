import React from 'react'
import createHistory from "history/createHashHistory"
import jquery from 'jquery'
import { Table, NavLink, Card, CardTitle, CardText, Button } from 'reactstrap';

const history = createHistory();

class EventItem extends React.Component {
        constructor(props) {
                super(props);
                this.onEdit = this.onEdit.bind(this);
                this.onDelete = this.onDelete.bind(this);
        }

        onEdit(){
                this.props.onEdit(this.props.event);
        }

        onDelete(){
                this.props.onDelete(this.props.event);
        }

        render(){
                return (
                  <div className='event-item'>
                      <div className='event-title'>{this.props.event.title}</div>
                      <div className='event-bt' onClick={this.onEdit}><i class="material-icons md-light">edit</i></div>
                      <div className='event-bt' onClick={this.onDelete}><i class="material-icons md-light">delete</i></div>
                  </div>)
        }
}

module.exports = EventItem;
