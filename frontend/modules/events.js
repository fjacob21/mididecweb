import React from 'react'

class Events extends React.Component{
        constructor(props) {
                super(props);
                console.debug('Start');
                this.state = {event: null, invalid: true};
                $.ajax({
                type: 'GET',
                url: "/mididec/api/v1.0/events/"+ this.props.match.params.id,
                success: this.success.bind(this),
                error: this.error,
                contentType: "application/json",
                dataType: 'json'
                });
        }

        success(data){
                this.state.event = data.event;
                this.state.invalid = false;
                this.setState(this.state);
        }

        error(){

        }

        render(){
                if (this.state.event != null) {
                        var start  = new Date(this.state.event.start);
                        var end  = new Date(this.state.event.end);
                        var dateOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
                        var timeOptions = { hour: 'numeric', minute: 'numeric', second: undefined};
                        var dateText = start.toLocaleDateString('fr-CA', dateOptions);
                        var timeText = start.toLocaleTimeString('fr-CA', timeOptions) + ' à ';
                        timeText += end.toLocaleTimeString('fr-CA', timeOptions);
                        var icalurl = '/mididec/api/v1.0/events/' + this.props.match.params.id + '/ical';
                return (
                        <div className='event'>
                                <div className='head'>
                                        <div className='start'> {start.toLocaleDateString('fr-CA', dateOptions)} </div>
                                        <div className='title'> <h1>{this.state.event.title} </h1></div>
                                        <div className='organizer'> Organiser par {this.state.event.organizer_name} </div>
                                </div>
                                <div className='body'>
                                        <div className='detail'>
                                                <div className='detaillabel'> Détail </div>
                                                <div className='description'>{this.state.event.description} </div>
                                        </div>
                                        <div className='info'>
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
                                                                {this.state.event.location}
                                                        </div>
                                                </div>
                                        </div>
                                </div>
                        </div>)
                }
                else {
                        if (this.state.invalid) {
                                return (
                                        <div className='event'>
                                                <div>Invalid Event </div>
                                        </div>)
                        }
                        return (
                                <div className='event'>
                                        <div> </div>
                                </div>)
                }
        }
}

module.exports = Events;
