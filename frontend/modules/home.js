import React from 'react'
import jquery from 'jquery'
import EventSummary from './eventsummary'
import { Table, NavLink, Card, CardTitle, CardText, Button } from 'reactstrap';
import createHistory from "history/createHashHistory"

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

        error(){

        }

        onEventDetails(event_id){
                history.push("/events/"+event_id);
        }

        render(){
                const n = new Date();
                const next = this.state.events.events.filter(event => new Date(event.start) >= n);
                const prev = this.state.events.events.filter(event => new Date(event.start) < n);
                var nextItems = <div className='nothing-label'>Aucun</div>;
                if(next.length > 0) {
                    nextItems = next.map((event) =>
                            <EventSummary key={event.event_id} event={event} />
                      );
                }
                var prevItems = <div className='nothing-label'>Aucun</div>;
                if(prev.length > 0) {
                    prevItems = prev.map((event) =>
                          <EventSummary key={event.event_id} event={event} />
                    );
                }
                return (
                        <div className='home'>
                            <Card body className='home-card'>
                                <CardTitle>Prochains Événements</CardTitle>
                                {nextItems}
                            </Card>
                            <Card body className='home-card'>
                                <CardTitle>Événements précédents</CardTitle>
                                {prevItems}
                            </Card>
                        </div>)
        }
}

module.exports = Home;
