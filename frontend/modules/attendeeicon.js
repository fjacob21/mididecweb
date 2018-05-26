import React from 'react'
import jquery from 'jquery'
import { Card, CardBody, CardTitle, Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';


class AttendeeIcon extends React.Component{

        constructor(props) {
                super(props);
        }

        render(){
                var avatar = <i className="material-icons md-light attendee-avatar-default">account_circle</i>
                console.debug(this.props.attendee);
                if (this.props.attendee.have_avatar) {
                        console.debug('have avatar');
                        var avatar_path = "/mididec/api/v1.0/users/" + this.props.attendee.user_id+"/avatar?" + new Date().getTime();
                        avatar = <img src={avatar_path} className="attendee-avatar"/>
                }
                return (
                        <div className='attendeeicon'>
                                {avatar}
                                {this.props.attendee.alias}
                        </div>
                );
        }
}

module.exports = AttendeeIcon;
