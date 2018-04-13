import React from 'react'
import jquery from 'jquery'
import EventSmall from './eventsmall'
import EventBig from './eventbig'

class Events extends React.Component{
        constructor(props) {
                super(props);
                console.debug('Start');
                this.state = {event: null, invalid: true};
                jquery.ajax({
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
                        return (
                                <div className='events'>
                                        <EventSmall event={this.state.event} />
                                        <EventBig event={this.state.event} />
                                </div>
                        );
                }
                else {
                        return (
                                <div className='event'>
                                </div>)

                }
        }
}

module.exports = Events;
