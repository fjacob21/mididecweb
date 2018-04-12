import React from 'react'
import createHistory from "history/createHashHistory"
import DateFormater from './dateformater'

const history = createHistory();

class EventSummary extends React.Component {
        constructor(props) {
                super(props);
        }

        onEventDetails(uid, isItem){
            if (!isItem || window.innerWidth < 500)
                history.push("/events/"+uid);
        }

        render(){
          var df = new DateFormater(this.props.event.start);
          var start = df.getDateText();
          var time = df.getTimeText();
          return (
                  <div className='event-summary' onClick={(e) => this.onEventDetails(this.props.event.uid, true)}>
                      <div className='es-title'>{this.props.event.title}</div>
                      <div className='es-start-long'>{start + ' ' + time}</div>
                      <div className='es-detail'><div className='event-detail-link' onClick={(e) => this.onEventDetails(this.props.event.uid, false)}>Détails</div></div>
                  </div>)
        }
}

module.exports = EventSummary;
