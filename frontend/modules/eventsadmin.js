import React from 'react'
import jquery from 'jquery'
import User from './user'
import Event from './event'
import EventItem from './eventitem'
import { Table, NavLink, Card, CardTitle, CardText, Button, Modal, ModalHeader, ModalBody, ModalFooter  } from 'reactstrap';
import createHistory from "history/createHashHistory"

const history = createHistory();

class EventsAdmin extends React.Component{
        constructor(props) {
                super(props);
                this.state = {events: {count:0, events:[]}, invalid: true, modal: false};
                this.onEdit = this.onEdit.bind(this);
                this.onDelete = this.onDelete.bind(this);
                this.rmSuccess = this.rmSuccess.bind(this);
                this.rmError = this.rmError.bind(this);
                this.onAccept = this.onAccept.bind(this);
                this.onRefuse = this.onRefuse.bind(this);
                this.updateEvents();

        }

        updateEvents(){
                var user = User.getSession();
                jquery.ajax({
                type: 'GET',
                url: "/mididec/api/v1.0/events?loginkey="+user.loginkey,
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

        onEdit(event){
                history.push("/events/"+event.event_id+"/update");
        }

        onDelete(event){
                this.state.modal = true;
                this.state.modalEvent = event;
                this.setState(this.state);
        }

        rmSuccess(data){
                this.updateEvents();
        }

        rmError(data){

        }

        onAccept(){
                var loguser = User.getSession();

                jquery.ajax({
                type: 'DELETE',
                url: "/mididec/api/v1.0/events/"+this.state.modalEvent.event_id,
                data: JSON.stringify ({loginkey: loguser.loginkey}),
                success: this.rmSuccess,
                error: this.rmError,
                contentType: "application/json",
                dataType: 'json'
                });
                this.state.modal = false;
                this.setState(this.state);
        }

        onRefuse(){
                this.state.modal = false;
                this.state.modalEvent = null;
                this.setState(this.state);
        }

        render(){
                var loguser = User.getSession();
                const eventslist = this.state.events.events.filter(event => loguser.isSuperUser || (loguser.isManager && event.owner_id==loguser.user_id));
                var events = eventslist.map(event =>
                  <EventItem event={event} onDelete={this.onDelete} onEdit={this.onEdit}/>
                );
                return (
                        <div className='eventsadmin'>
                                <Card body className='events-card'>
                                        <CardTitle>Events</CardTitle>
                                        {events}
                                </Card>
                                <Modal isOpen={this.state.modal}>
                                        <ModalHeader toggle={this.toggle}>Modal title</ModalHeader>
                                        <ModalBody>
                                                Etes-vous sur de vouloir effacer cette rencontre?
                                        </ModalBody>
                                        <ModalFooter>
                                                <Button color="primary" onClick={this.onAccept}>Oui</Button>{' '}
                                                <Button color="secondary" onClick={this.onRefuse}>Non</Button>
                                        </ModalFooter>
                                </Modal>

                        </div>)
        }
}

module.exports = EventsAdmin;
