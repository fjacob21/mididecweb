import React from 'react'
import DateFormater from './dateformater'
import User from './user'
import RegisterPanel from './registerpanel'
import RegisterStatusPanel from './registerstatuspanel'
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';

class EventSmall extends React.Component{
        constructor(props) {
                super(props);
                this.state = {
                      valid: false,
                      modal: false,
                      userinfo: null
                };
                this._start = new DateFormater(this.props.event.start);
                this._end = new DateFormater(this.props.event.end);
                this.onCancel = this.onCancel.bind(this);
                this.onRegister = this.onRegister.bind(this);
                this.onUserInfoChange = this.onUserInfoChange.bind(this);
        }

        onCancel() {
                this.state.modal = false;
                this.setState(this.state);
        }

        onRegister(){
                this.state.modal = false;
                this.setState(this.state);
                this.props.onRegister(this.state.userinfo);
        }

        onUserInfoChange(obj, userinfo){
                this.state.userinfo = obj;
                this.state.valid = false;
                var at = obj.email.indexOf('@');
                var dot = obj.email.indexOf('.');
                if (obj.name != '' && obj.email != '' && at != -1 && dot != -1 && at < dot && dot+1 < obj.email.length )
                        this.state.valid = true;
                this.setState(this.state);
        }

        render(){
                var user = User.getSession();
                var dateText = this._start.getDateText();
                var timeText = this._start.getTimeText() + ' à ';
                timeText += this._end.getTimeText();
                var icalurl = '/mididec/api/v1.0/events/' + this.props.event.event_id + '/ical';
                var registerPanel = <RegisterPanel onRegister={this.onRegister}/>
                if (this.props.event.find_attendee(user))
                    registerPanel = <RegisterStatusPanel status='attending' onCancel={this.onCancel} />
                else if (this.props.event.find_waiting(user))
                    registerPanel = <RegisterStatusPanel status='waiting' onCancel={this.onCancel} />
                return (
                        <div className='eventsmall'>
                                <div className='title'>{this.props.event.title}</div>

                                <div className='detail'>
                                        <div className='detaillabel'> Détail </div>
                                        <div className='description'>{this.props.event.description} </div>
                                </div>
                                <div className='register'>
                                        {registerPanel}
                                </div>
                                <div className='duration'>
                                        <img className='timeicon' src='res/drawables/time-icon.png'></img>
                                        <div className='timetext'>
                                                <div className='date'>{dateText}</div>
                                                <div className='time'>{timeText}</div>
                                                <a href={icalurl}>Ajouter au calendrier</a>
                                        </div>
                                </div>
                                <div className='location'>
                                        <img className='locationicon' src='res/drawables/location-icon.png'></img>
                                        <div className='locationtext'>
                                                {this.props.event.location}
                                        </div>
                                </div>
                        </div>);
        }
}

module.exports = EventSmall;
