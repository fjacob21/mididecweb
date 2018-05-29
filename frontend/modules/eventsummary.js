import React from 'react'
import createHistory from "history/createHashHistory"
import DateFormater from './dateformater'
import { Card, CardTitle } from 'reactstrap';

const history = createHistory();

class EventSummary extends React.Component {
        constructor(props) {
                super(props);
        }

        onEventDetails(event_id, isItem){
                history.push("/events/"+event_id);
        }

        render(){
          var df = new DateFormater(this.props.event.start);
          var start = df.getDateText();
          var time = df.getTimeText();
          var attendeesNumber = this.props.event.attendees.length;
          var attendeesLeft = this.props.event.max_attendee - attendeesNumber;
          return (
                  <div className='event-summary' onClick={(e) => this.onEventDetails(this.props.event.event_id, true)}>
                        <Card body className='home-card'>
                                <CardTitle><div className='es-title'>{this.props.event.title}</div></CardTitle>
                                <div className='es-start-long'>{start + ' ' + time}</div>
                                <div className='es-attendees'>{attendeesNumber} personnes inscrites - <font color="red">{attendeesLeft} places disponibles</font></div>
                        </Card>
                  </div>)
        }
}

module.exports = EventSummary;
