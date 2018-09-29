import React from 'react'
import DateFormater from './dateformater'
import User from './user'
import RegisterPanel from './registerpanel'
import RegisterStatusPanel from './registerstatuspanel'
import AttendeeIcon from './attendeeicon'
import Text from './localization/text'
import Autolinker from 'autolinker'
import { Alert } from 'reactstrap';

class EventBig extends React.Component{
        constructor(props) {
                super(props);
                this._start = new DateFormater(this.props.event.start);
                this._end = new DateFormater(this.props.event.end);
                this.onCancel = this.onCancel.bind(this);
                this.onRegister = this.onRegister.bind(this);
        }

        onCancel() {
                this.props.onCancel();
        }

        onRegister(){
                this.props.onRegister();
        }

        render(){
                var user = User.getSession();
                var dateText = this._start.getDateText();
                var timeText = this._start.getTimeText() + ' à ';
                timeText += this._end.getTimeText();
                var icalurl = '/mididec/api/v1.0/events/' + this.props.event.event_id + '/ical';
                var linkedText = Autolinker.link( this.props.event.description );
                linkedText = {__html: linkedText};
                var attendees = "";
                if (user && this.props.event.attendees.length) {
                    var attendeeslist = this.props.event.attendees.map((attendee) =>
                            <AttendeeIcon key={attendee.user_id} attendee={attendee} className='attendee-icon'/>
                    );
                    attendees = (<div><div className='attendees-title'>{Text.text.event_attendees_label}({this.props.event.attendees.length})</div>
                    <div className='attendeesgrid'>
                            {attendeeslist}
                    </div></div>);
                }
                var eventurl = '/mididec/api/v1.0/events/' + this.props.event.event_id + "/attachments/";
                var attachments = "";
                if (user && this.props.event.attachments.length){
                    var attachmentslist = this.props.event.attachments.map((attachment) =>
                            <a key={attachment} href={eventurl+attachment} className='attachment-item'>{attachment}</a>
                    );
                    attachments = (<div><div className='attachments-title'>{Text.text.event_attachments_label}</div>
                    <div className='attachmentsgrid'>
                            {attachmentslist}
                    </div></div>);
                }
                var waintings = '';
                if (user && (user.isManager || user.isSuperUser) && this.props.event.waitings.length) {
                  var waitingslist = this.props.event.waitings.map((waiting) =>
                          <AttendeeIcon key={waiting.user_id} attendee={waiting} className='attendee-icon'/>
                  );
                  waintings = (<div><div className='attendees-title'>{Text.text.event_waitings_label}({this.props.event.waitings.length})</div>
                  <div className='attendeesgrid'>
                          {waitingslist}
                  </div></div>);
                }
                var notTraining = '';
                if (this.props.event.not_training)
                  notTraining = (<Alert className='error' color='danger' isOpen='true' transitionappeartimeout={150} transitionappeartimeout={150}>
                        {Text.text.event_not_training_label}
                </Alert>);
                var registerPanel = <RegisterPanel onRegister={this.onRegister} disabled={this.props.disableRegister}/>
                if (this.props.event.find_attendee(user))
                    registerPanel = <RegisterStatusPanel status='attending' onCancel={this.onCancel} disabled={this.props.disableRegister}/>
                else if (this.props.event.find_waiting(user))
                    registerPanel = <RegisterStatusPanel status='waiting' onCancel={this.onCancel} disabled={this.props.disableRegister} />
                return (
                        <div className='eventbig'>
                                {notTraining}
                                <div className='head'>
                                        <div className='head-info'>
                                                <div className='start'> {dateText} </div>
                                                <div className='title'> {this.props.event.title} </div>
                                                <div className='organizer'> {Text.text.event_organizer_label} {this.props.event.organizer_name} </div>
                                        </div>
                                        <div className='head-register'>
                                                {registerPanel}
                                        </div>
                                </div>
                                <div className='body'>
                                        <div className='detail'>
                                                <div className='detaillabel'> {Text.text.event_details_label} </div>
                                                <div className='description' dangerouslySetInnerHTML={linkedText}/>
                                                {attendees}
                                                {waintings}
                                                {attachments}
                                        </div>
                                        <div className='info'>
                                                <div className='duration'>
                                                        <img className='timeicon' src='res/drawables/time-icon.png'></img>
                                                        <div className='timetext'>
                                                                <div className='date'>{dateText}</div>
                                                                <div className='time'>{timeText}</div>
                                                                <a href={icalurl}>{Text.text.event_add_to_calendar_label}</a>
                                                        </div>
                                                </div>
                                                <div className='location'>
                                                        <img className='locationicon' src='res/drawables/location-icon.png'></img>
                                                        <div className='locationtext'>
                                                                {this.props.event.location}
                                                        </div>
                                                </div>
                                        </div>
                                </div>
                        </div>);
        }
}

module.exports = EventBig;
