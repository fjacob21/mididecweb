import React from 'react'
import jquery from 'jquery'
import { Card, CardBody, CardTitle, Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';


class AttendeeIcon extends React.Component{

        constructor(props) {
                super(props);
        }

        render(){
                return (
                        <div className='attendeeicon'>
                                <i class="material-icons md-light attendee-avatar">account_circle</i>
                                {this.props.attendee.alias}
                        </div>
                );
        }
}

module.exports = AttendeeIcon;
