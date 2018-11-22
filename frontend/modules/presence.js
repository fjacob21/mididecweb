import React from 'react'
import Event from './event'
import jquery from 'jquery'
import User from './user'
import createHistory from "history/createHashHistory"
import AttendeeIcon from './attendeeicon'
import Errors from './errors'
import { Input, Button } from 'reactstrap';
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
                this.onCheck = this.onCheck.bind(this);
                this.success = this.success.bind(this);
                this.error = this.error.bind(this);
        }

        success(data){
                console.debug(data);
                this.state.event = new Event(data.event);
                this.state.invalid = false;
                this.setState(this.state);
        }

        error(data){
                var errorCode = data.responseJSON.code;
                this.showAlert(Errors.getErrorMessage(errorCode), 'danger');
        }

        onCheck(e){
                console.debug(e.target.id);
                var user = User.getSession();
                var data = {'user_id': e.target.id, 'present': e.target.checked, 'loginkey': user.loginkey};
                jquery.ajax({
                        type: 'POST',
                        url: "/mididec/api/v1.0/events/" + this.props.match.params.id + '/present',
                        data: JSON.stringify (data),
                        success: this.success,
                        error: this.error,
                        contentType: "application/json",
                        dataType: 'json'
                        });
        }

        onPrint() {
                var user = User.getSession();
                var presencesurl = '/mididec/api/v1.0/events/' + this.state.event.event_id + '/presences?loginkey='+user.loginkey;
                window.open(presencesurl, 'blank');
        }

        showAlert(message, color='success'){
                this.props.onError(message, color);
        }

        render(){
                var user = User.getSession();
                var attendees = "";
                var presencesurl = "";
                if (user && this.state.event){
                        var attendees = this.state.event.attendees.filter(attendee => attendee.name != '');
                        attendees.sort(function(a, b){
                                if (a.name > b.name) {return 1;}
                                if (a.name < b.name) {return -1;}
                                return 0;
                            });
                        attendees = attendees.map((attendee) =>
                                <div key={attendee.user_id} className='presence-item'>
                                <div className='presence-icon-item'><AttendeeIcon className='presence-icon' attendee={attendee} noname/></div>
                                <div className='presence-name-item'>{attendee.name}</div>
                                <div className='presence-present-item'><Input className='presence-present-cb-item' onChange={this.onCheck} type='checkbox' id={attendee.user_id} checked={attendee.present} /></div>
                                <div className='presence-present-time-item'>{attendee.presentTime}</div>
                                </div>
                    );
                }
                return (
                        <div className='presence'>
                                <div className='presence-title'>{Text.text.presence}</div>
                                <div className='presence-item'>
                                        <div className='presence-icon-item'></div>
                                        <div className='presence-name-item'>{Text.text.name}</div>
                                        <div className='presence-present-item'>{Text.text.presences}</div>
                                        <div className='presence-present-time-item'>{Text.text.present_time}</div>
                                </div>
                                {attendees}
                                <Button color="warning" onClick={this.onPrint}>{Text.text.print}</Button>
                        </div>
                );
        }
}

module.exports = Presence;
