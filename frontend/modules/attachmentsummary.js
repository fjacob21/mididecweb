import React from 'react'
import createHistory from "history/createHashHistory"
import jquery from 'jquery'
import User from './user'
import { Table, NavLink, Card, CardTitle, CardText, Button } from 'reactstrap';

const history = createHistory();

class AttachmentSummary extends React.Component {
        constructor(props) {
                super(props);
                this.onDelete = this.onDelete.bind(this);
        }

        onDelete(){
                this.props.onDelete(this.props.attachment);
        }

        render(){
                var btRemove = <div className='attachment-bt' onClick={this.onDelete}><i className="material-icons md-light">delete</i></div>
                return (
                  <div className='attachment-summary'>
                      <div className='attachment-name'>{this.props.attachment}</div>
                      <div className='attachment-action'>
                              {btRemove}
                      </div>
                  </div>)
        }
}

module.exports = AttachmentSummary;
