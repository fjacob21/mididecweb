import React from 'react'
import Event from './event'
import jquery from 'jquery'
import User from './user'
import createHistory from "history/createHashHistory"
import AttendeeIcon from './attendeeicon'
import Errors from './errors'
import { Table } from 'reactstrap';
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

        showAlert(message, color='success'){
                this.props.onError(message, color);
        }

        render(){
                var user = User.getSession();
                var attendees = "";
                if (user && this.state.event)
                    attendees = this.state.event.attendees.map((attendee) =>
                            <tr key={attendee.user_id} className='attendee-item'>
                              <th className='presence-item'><AttendeeIcon className='presence-icon' attendee={attendee} noname/></th>
                              <td className='presence-item'>{attendee.name}</td>
                              <td className='presence-item'><div className='attendee-sign'></div></td>
                            </tr>
                    );
                    // <div className='attendee-item'>
                    //         <AttendeeIcon key={attendee.user_id} attendee={attendee} noname/>
                    //         <div>{attendee.name}</div>
                    //         <div className='attendee-sign'></div>
                    // </div>
                return (
                        <div className='presence'>
                                <div className='presence-title'>Présences</div>

                                <Table>
                                <thead>
                                  <tr>
                                    <th></th>
                                    <th>Nom</th>
                                    <th>Signature</th>
                                  </tr>
                                </thead>
                                <tbody>
                                {attendees}
                                {attendees}
                                {attendees}
                                {attendees}
                                {attendees}
                                {attendees}

                                </tbody>
                              </Table>
                        </div>
                );
        }
}

module.exports = Presence;
