import React from 'react'
import jquery from 'jquery'
import User from './user'
import Event from './event'
import EventItem from './eventitem'
import Errors from './errors'
import { Table, NavLink, Card, CardTitle, CardText, Button, Modal, ModalHeader, ModalBody, ModalFooter  } from 'reactstrap';
import createHistory from "history/createHashHistory"
import Text from './localization/text'

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

        error(data){
            var errorCode = data.responseJSON.code;
            this.showAlert(Errors.getErrorMessage(errorCode), 'danger');
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
                this.showAlert(Text.text.event_delete_success_msg, 'success');
                this.updateEvents();
        }

        rmError(data){
            var errorCode = data.responseJSON.code;
            this.showAlert(Errors.getErrorMessage(errorCode), 'danger');
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

        showAlert(message, color='success'){
                this.props.onError(message, color);
        }

        render(){
                var loguser = User.getSession();
                const eventslist = this.state.events.events.filter(event => loguser.isSuperUser || (loguser.isManager && event.owner_id==loguser.user_id));
                var events = eventslist.map(event =>
                  <EventItem event={event} onDelete={this.onDelete} onEdit={this.onEdit}/>
                );
                var modalTitle = "";
                if (this.state.modalEvent)
                        modalTitle = this.state.modalEvent.title;
                return (
                        <div className='eventsadmin'>
                                <Card body className='events-card'>
                                        <CardTitle>{Text.text.events_title}</CardTitle>
                                        {events}
                                </Card>
                                <Modal isOpen={this.state.modal}>
                                        <ModalHeader toggle={this.toggle}>{modalTitle}</ModalHeader>
                                        <ModalBody>
                                                {Text.text.event_delete_confirm_msg}
                                        </ModalBody>
                                        <ModalFooter>
                                                <Button color="primary" onClick={this.onAccept}>{Text.text.yes}</Button>{' '}
                                                <Button color="secondary" onClick={this.onRefuse}>{Text.text.no}</Button>
                                        </ModalFooter>
                                </Modal>

                        </div>)
        }
}

module.exports = EventsAdmin;
