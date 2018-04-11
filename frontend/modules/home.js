import React from 'react'
import jquery from 'jquery'
import { Table, NavLink } from 'reactstrap';
import createHistory from "history/createHashHistory"

const history = createHistory();

class Home extends React.Component{
        constructor(props) {
                super(props);
                this.state = {events: [], invalid: true};
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

        onEventDetails(uid){
                console.log(uid);
                history.push("/events/"+uid);
        }

        render(){
                const listItems = this.state.events.map((event) =>
                        <tr>
                          <th>{event.title}</th>
                          <td>{event.start}</td>
                          <td><div className='event-detail-link' onClick={(e) => this.onEventDetails(event.uid)}>Détails</div></td>
                        </tr>
                  );
                return (
                        <div className='home'>
                                <Table>
                                        <thead>
                                          <tr>
                                            <th>Titre</th>
                                            <th>Date</th>
                                            <th></th>
                                          </tr>
                                        </thead>
                                        <tbody>
                                          {listItems}
                                        </tbody>
                                </Table>
                        </div>)
        }
}

module.exports = Home;
