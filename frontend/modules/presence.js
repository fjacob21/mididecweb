import React from 'react'
import Event from './event'
import jquery from 'jquery'
import User from './user'
import createHistory from "history/createHashHistory"
import AttendeeIcon from './attendeeicon'
import Errors from './errors'
import { Table, Button } from 'reactstrap';
import Text from './localization/text'
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
                var user = User.getSession();
                var loginkey = ""
                if (user)
                  loginkey = "?loginkey=" + user.loginkey
                jquery.ajax({
                type: 'GET',
                url: "/mididec/api/v1.0/events/"+ this.props.match.params.id + loginkey,
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
                                <div className='presence-title'>{Text.text.presence}</div>
                                <div className='presence-item'>
                                        <div className='presence-icon-item'></div>
                                        <div className='presence-name-item'>{Text.text.name}</div>
                                        <div className='presence-sign-item'>{Text.text.signature}</div>
                                </div>
                                {attendees}
                                <Button color="warning" onClick={this.onPrint}>{Text.text.print}</Button>
                        </div>
                );
        }
}

module.exports = Presence;
