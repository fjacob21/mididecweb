import React from 'react'
import jquery from 'jquery'
import User from './user'
import createHistory from "history/createHashHistory"
import Errors from './errors'
import FormQuery from './formquery'
import { Button, Form, FormGroup, Label, Input } from 'reactstrap';

const history = createHistory();

class UpdateEvent extends React.Component{
        constructor(props) {
            super(props);
            var user = User.getSession();
            this.state = {
                  valid: false,
                  values: { title: '',
                      description: '',
                      max_attendee: '20',
                      startDate: '',
                      time: '12:00',
                      durationString: '1h00',
                      location: '3b6',
                      organizer_name: user.alias,
                      organizer_email: user.email}
            };
            var user = User.getSession();
            jquery.ajax({
            type: 'GET',
            url: "/mididec/api/v1.0/events/"+ this.props.match.params.id+'?loginkey='+user.loginkey,
            success: this.success.bind(this),
            error: this.error.bind(this),
            contentType: "application/json",
            dataType: 'json'
            });
            this.onCancel = this.onCancel.bind(this);
            this.onUpdate = this.onUpdate.bind(this);
            this.onChange = this.onChange.bind(this);
            this.updateSuccess = this.updateSuccess.bind(this);
            this.updateError = this.updateError.bind(this);
            this.onPublish = this.onPublish.bind(this);
            this.publishSuccess = this.publishSuccess.bind(this);
            this.publishError = this.publishError.bind(this);
            this.onKeyPress = this.onKeyPress.bind(this);
        }

        success(data){

                this.state.values = data.event;
                var d = new Date(this.state.values.start);
                var dateParts = this.state.values.start.split('T');
                this.state.values.startDate = dateParts[0];
                var time = dateParts[1].substring(0, dateParts[1].length-1);
                this.state.values.time = time;
                var durationHour = Math.floor(this.state.values.duration / 3600);
                var durationMinute = (this.state.values.duration - (durationHour*3600))/60;
                this.state.values.durationString = durationHour.toString() + 'h' + durationMinute.toString();
                this.state.invalid = false;
                this.setState(this.state);
        }

        error(data){
                var errorCode = data.responseJSON.code;
                this.showAlert(Errors.getErrorMessage(errorCode), 'danger');
        }

        updateSuccess(data){
            this.showAlert('l\'événement a été enregistré', 'success')
        }

        updateError(data){
            var errorCode = data.responseJSON.code;
            this.showAlert(Errors.getErrorMessage(errorCode), 'danger');
        }

        showAlert(message, color='success'){
                this.props.onError(message, color);
        }

        parseDate(date, time){
            var tparts = time.split(' ');
            var h = parseInt(tparts[0].split(':')[0]);
            var m = parseInt(tparts[0].split(':')[1]);
            m = ("0" + m).slice(-2);
            if (tparts[1] == 'PM')
                h += 12;
            return date + 'T' + h+':'+m+':00Z';
        }

        parseDuration(duration){
            var durParts = duration.split('h');
            var h = parseInt(durParts[0]);
            var m = parseInt(durParts[1]);
            return (m*60) + (h * 3600);
        }

        onUpdate() {
            this.state.values.start = this.parseDate(this.state.values.startDate, this.state.values.time);
            this.state.values.duration = this.parseDuration(this.state.values.durationString);
            var user = User.getSession();
            this.state.values['loginkey'] = user.loginkey
            this.state.valid = false;
            this.setState(this.state);
            jquery.ajax({
            type: 'POST',
            url: "/mididec/api/v1.0/events/" + this.props.match.params.id,
            data: JSON.stringify (this.state.values),
            success: this.updateSuccess,
            error: this.updateError,
            contentType: "application/json",
            dataType: 'json'
            });
        }

        onCancel() {
                history.goBack();
        }

        onPublish() {
            var user = User.getSession();
            this.state.values['loginkey'] = user.loginkey
            jquery.ajax({
            type: 'POST',
            url: "/mididec/api/v1.0/events/" + this.props.match.params.id + '/publish',
            data: JSON.stringify (this.state.values),
            success: this.publishSuccess,
            error: this.publishError,
            contentType: "application/json",
            dataType: 'json'
            });
        }

        publishSuccess(data){
            this.showAlert('l\'événement a été publié', 'success')
        }

        publishError(data){
                this.showAlert('Une erreur est survenue lors de la publicaion de l\'événement!', 'danger')
        }

        onChange(e) {
                this.state.valid = false;
                if (FormQuery.isIos()) {
                        var fq = new FormQuery(this.state.values);
                        this.state.values = fq.parse();
                }
                else {
                        this.state.values[e.target.id] = e.target.value;
                }
                var n = new Date(Date.now());
                var start = new Date(this.state.values.startDate + "T" + this.state.values.time + 'Z');
                start = new Date(start.setTime( start.getTime() + start.getTimezoneOffset()*60*1000 ));
                var isBefore = n > start;
                if (this.state.values.title != '' && this.state.values.description != '' && this.state.values.startDate != '' && !isBefore)
                        this.state.valid = true;
                this.setState(this.state);
        }

        onKeyPress(e){
                if (e.key == 'Enter' && this.state.valid)
                        this.onAdd();
        }

        render() {
            return (
                <div className='createevent'>
                    <Form className='form' onKeyPress={this.onKeyPress}>
                            <FormGroup className='title'>
                                    <Label for="title">Titre <font size="3" color="red">*</font></Label>
                                    <Input onChange={this.onChange} type='text' name="title" id="title" placeholder="title" value={this.state.values.title} />
                            </FormGroup>
                            <FormGroup className='description'>
                                    <Label for="description">Description <font size="3" color="red">*</font></Label>
                                    <Input onChange={this.onChange} type='textarea' name="description" id="description" placeholder="description" value={this.state.values.description} />
                            </FormGroup>
                            <FormGroup className='startDate'>
                                    <Label for="startDate">Début <font size="3" color="red">*</font></Label>
                                    <div><Input onChange={this.onChange} type='date' name="startDate" id="startDate" placeholder="startDate" value={this.state.values.startDate} />
                                    <Input onChange={this.onChange} type='time' name="time" id="time" placeholder="time" value={this.state.values.time} /></div>
                            </FormGroup>
                            <FormGroup className='durationString'>
                                    <Label for="durationString">Durée </Label>
                                    <Input onChange={this.onChange} type='text' name="durationString" id="durationString" placeholder="durationString" value={this.state.values.durationString} />
                            </FormGroup>
                            <FormGroup className='max_attendee'>
                                    <Label for="max_attendee">Nombre de participants</Label>
                                    <Input onChange={this.onChange} type='text' name="max_attendee" id="max_attendee" placeholder="20" value={this.state.values.max_attendee} />
                            </FormGroup>
                            <FormGroup className='location'>
                                    <Label for="location">location</Label>
                                    <Input onChange={this.onChange} type='text' name="location" id="location" placeholder="location" value={this.state.values.location} />
                            </FormGroup>
                            <FormGroup className='organizer_name'>
                                    <Label for="organizer_name">Organisateur</Label>
                                    <Input onChange={this.onChange} type='text' name="organizer_name" id="organizer_name" placeholder="organizerName" value={this.state.values.organizer_name} />
                            </FormGroup>
                            <FormGroup className='organizer_email'>
                                    <Label for="organizer_email">Courriel de l'Organisateur</Label>
                                    <Input onChange={this.onChange} type='email' name="organizer_email" id="organizer_email" placeholder="organizer_email" value={this.state.values.organizer_email} />
                            </FormGroup>
                            <Button color="primary" onClick={this.onUpdate} disabled={!this.state.valid}>Sauvegarder</Button>{' '}
                            <Button color="secondary" onClick={this.onCancel}>Cancel</Button>{' '}
                            <Button color="warning" onClick={this.onPublish}>Publier</Button>
                    </Form>
                </div>)
        }
}

module.exports = UpdateEvent;
