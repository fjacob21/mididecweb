import React from 'react'
import Event from './event'
import jquery from 'jquery'
import User from './user'
import createHistory from "history/createHashHistory"
import AttendeeIcon from './attendeeicon'
import Errors from './errors'
import { Table, Button } from 'reactstrap';
var PrintTemplate = require ('react-print');

const history = createHistory();

class Presence extends React.Component{
        constructor(props) {
                super(props);
                this.state = {
                        event: null,
                        invalid: true,
                        disableRegister: false
                        };
                jquery.ajax({
                type: 'GET',
                url: "/mididec/api/v1.0/events/"+ this.props.match.params.id,
                success: this.success.bind(this),
                error: this.error.bind(this),
                contentType: "application/json",
                dataType: 'json'
                });
                this.onPrint = this.onPrint.bind(this);
        }

        success(data){
                this.state.event = new Event(data.event);
                this.state.invalid = false;
                this.setState(this.state);
        }

        error(data){
                var errorCode = data.responseJSON.code;
                this.showAlert(Errors.getErrorMessage(errorCode), 'danger');
        }

        onPrint() {
                window.print();
        }

        showAlert(message, color='success'){
                this.props.onError(message, color);
        }

        render(){
                var user = User.getSession();
                var attendees = "";
                if (user && this.state.event)
                    attendees = this.state.event.attendees.map((attendee) =>
                            <div key={attendee.user_id} className='presence-item'>
                              <div className='presence-icon-item'><AttendeeIcon className='presence-icon' attendee={attendee} noname/></div>
                              <div className='presence-name-item'>{attendee.name}</div>
                              <div className='presence-sign-item'><div className='presence-sign'></div></div>
                            </div>
                    );
                return (
                        <div className='presence'>
                                <div className='presence-title'>Présences</div>
                                <div className='presence-item'>
                                        <div className='presence-icon-item'></div>
                                        <div className='presence-name-item'>Nom</div>
                                        <div className='presence-sign-item'>Signature</div>
                                </div>
                                {attendees}
                                <Button color="warning" onClick={this.onPrint}>Imprimer</Button>
                        </div>
                );
        }
}

module.exports = Presence;
