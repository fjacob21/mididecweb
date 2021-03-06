import React from 'react'
import jquery from 'jquery'
import EventSummary from './eventsummary'
import Errors from './errors'
import createHistory from "history/createHashHistory"
import Text from './localization/text'

const history = createHistory();

class Home extends React.Component{
        constructor(props) {
                super(props);
                this.state = {events: {count:0, events:[]}, invalid: true};
                jquery.ajax({
                type: 'GET',
                url: "/mididec/api/v1.0/events",
                success: this.success.bind(this),
                error: this.error.bind(this),
                contentType: "application/json",
                dataType: 'json'
                });
        }

        success(data){
                this.state.events = data.events;
                this.state.invalid = false;
                this.setState(this.state);
        }

        error(data){
            var errorCode = data.responseJSON.code;
            this.showAlert(Errors.getErrorMessage(errorCode), 'danger');
        }

        onEventDetails(event_id){
                history.push("/events/"+event_id);
        }

        render(){
                const n = new Date();
                var next = this.state.events.events.filter(event => new Date(event.start) >= n);
                var prev = this.state.events.events.filter(event => new Date(event.start) < n);
                next.sort(function(a, b){
                        var x = new Date(a.start);
                        var y = new Date(b.start);
                        if (x < y) {return 1;}
                        if (x > y) {return -1;}
                        return 0;
                    });
                prev.sort(function(a, b){
                        var x = new Date(a.start);
                        var y = new Date(b.start);
                        if (x < y) {return 1;}
                        if (x > y) {return -1;}
                        return 0;
                        });
                var nextItems = <div className='nothing-label'>{Text.text.none}</div>;
                if(next.length > 0) {
                    nextItems = next.map((event) =>
                            <EventSummary key={event.event_id} event={event} />
                      );
                }
                var prevItems = <div className='nothing-label'>{Text.text.none}</div>;
                if(prev.length > 0) {
                    prevItems = prev.map((event) =>
                          <EventSummary key={event.event_id} event={event} />
                    );
                }
                return (
                        <div className='home'>
                                <div className='next-events'>{Text.text.next_events}</div>
                                {nextItems}
                                <div className='next-events'>{Text.text.previous_events}</div>
                                {prevItems}
                        </div>)
        }
}

module.exports = Home;
