import React from 'react'
import DateFormater from './dateformater'

class EventSmall extends React.Component{
        constructor(props) {
                super(props);
                this._start = new DateFormater(this.props.event.start);
                this._end = new DateFormater(this.props.event.end);
        }

        render(){
                var dateText = this._start.getDateText();
                var timeText = this._start.getTimeText() + ' à ';
                timeText += this._end.getTimeText();
                var icalurl = '/mididec/api/v1.0/events/' + this.props.event.uid + '/ical';
                return (
                        <div className='eventsmall'>
                                <div className='title'>{this.props.event.title}</div>

                                <div className='detail'>
                                        <div className='detaillabel'> Détail </div>
                                        <div className='description'>{this.props.event.description} </div>
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
