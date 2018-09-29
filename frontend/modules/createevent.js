import React from 'react'
import jquery from 'jquery'
import User from './user'
import createHistory from "history/createHashHistory"
import Errors from './errors'
import FormQuery from './formquery'
import { Button, Form, FormGroup, Label, Input } from 'reactstrap';
import Text from './localization/text'

const history = createHistory();

class CreateEvent extends React.Component{
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
                      organizer_email: user.email,
                      not_training: false
                     }
            };
            this.onCancel = this.onCancel.bind(this);
            this.onAdd = this.onAdd.bind(this);
            this.onChange = this.onChange.bind(this);
            this.addSuccess = this.addSuccess.bind(this);
            this.addError = this.addError.bind(this);
            this.onKeyPress = this.onKeyPress.bind(this);
            this.onBlur = this.onBlur.bind(this);
            this.onCheck = this.onCheck.bind(this);
        }

        addSuccess(data){
            this.props.onloading(false);
            this.showAlert(Text.text.event_add_success, 'success')
            history.replace("/events/" + data.event.event_id + '/update');
        }

        addError(data){
            this.props.onloading(false);
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

        onAdd() {
            this.props.onloading(true);
            this.state.values.start = this.parseDate(this.state.values.startDate, this.state.values.time);
            this.state.values.duration = this.parseDuration(this.state.values.durationString);
            var user = User.getSession();
            this.state.values['loginkey'] = user.loginkey
            this.state.valid = false;
            this.setState(this.state);
            jquery.ajax({
            type: 'POST',
            url: "/mididec/api/v1.0/events",
            data: JSON.stringify (this.state.values),
            success: this.addSuccess,
            error: this.addError,
            contentType: "application/json",
            dataType: 'json'
            });
        }

        onCancel() {
                history.goBack();
        }

        onCheck(e){
                this.state.values[e.target.id] = e.target.checked;
                this.setState(this.state);
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

        onBlur(e){
            if (FormQuery.isIos()) {
                    var fq = new FormQuery(this.state.values);
                    this.state.values = fq.parse();
                    var n = new Date(Date.now());
                    var start = new Date(this.state.values.startDate + "T" + this.state.values.time + 'Z');
                    start = new Date(start.setTime( start.getTime() + start.getTimezoneOffset()*60*1000 ));
                    var isBefore = n > start;
                    if (this.state.values.title != '' && this.state.values.description != '' && this.state.values.startDate != '' && !isBefore)
                            this.state.valid = true;
                    this.setState(this.state);
            }
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
                                    <Label for="title">{Text.text.event_title_label} <font size="3" color="red">*</font></Label>
                                    <Input onBlur={this.onBlur} onChange={this.onChange} type='text' name="title" id="title" placeholder="title" value={this.state.values.title} />
                            </FormGroup>
                            <FormGroup className='description'>
                                    <Label for="description">{Text.text.event_description_label} <font size="3" color="red">*</font></Label>
                                    <Input onBlur={this.onBlur} onChange={this.onChange} type='textarea' name="description" id="description" placeholder="description" value={this.state.values.description} />
                            </FormGroup>
                            <FormGroup className='startDate'>
                                    <Label for="startDate">{Text.text.event_start_date_label} <font size="3" color="red">*</font></Label>
                                    <div><Input onBlur={this.onBlur} onChange={this.onChange} type='date' name="startDate" id="startDate" placeholder="startDate" value={this.state.values.startDate} />
                                    <Input onBlur={this.onBlur} onChange={this.onChange} type='time' name="time" id="time" placeholder="time" value={this.state.values.time} /></div>
                            </FormGroup>
                            <FormGroup className='durationString'>
                                    <Label for="durationString">{Text.text.event_duration_label} </Label>
                                    <Input onBlur={this.onBlur} onChange={this.onChange} type='text' name="durationString" id="durationString" placeholder="durationString" value={this.state.values.durationString} />
                            </FormGroup>
                            <FormGroup className='max_attendee'>
                                    <Label for="max_attendee">{Text.text.event_max_attendee_label}</Label>
                                    <Input onBlur={this.onBlur} onChange={this.onChange} type='text' name="max_attendee" id="max_attendee" placeholder="20" value={this.state.values.max_attendee} />
                            </FormGroup>
                            <FormGroup className='location'>
                                    <Label for="location">{Text.text.event_location_label}</Label>
                                    <Input onBlur={this.onBlur} onChange={this.onChange} type='text' name="location" id="location" placeholder="location" value={this.state.values.location} />
                            </FormGroup>
                            <FormGroup className='organizer_name'>
                                    <Label for="organizer_name">{Text.text.event_organizer_name_label}</Label>
                                    <Input onBlur={this.onBlur} onChange={this.onChange} type='text' name="organizer_name" id="organizer_name" placeholder="organizerName" value={this.state.values.organizer_name} />
                            </FormGroup>
                            <FormGroup className='organizer_email'>
                                    <Label for="organizer_email">{Text.text.event_organizer_email_label}</Label>
                                    <Input onBlur={this.onBlur} onChange={this.onChange} type='email' name="organizer_email" id="organizer_email" placeholder="organizer_email" value={this.state.values.organizer_email} />
                            </FormGroup>
                            <FormGroup check>
                                    <Label>
                                            <Input onBlur={this.onBlur} onChange={this.onCheck} type='checkbox' id="not_training" checked={this.state.values.not_training} />
                                            {Text.text.event_not_training_label}
                                    </Label>
                            </FormGroup>
                            <Button color="primary" onClick={this.onAdd} disabled={!this.state.valid}>{Text.text.event_add_add_bt_label}</Button>{' '}
                            <Button color="secondary" onClick={this.onCancel}>{Text.text.cancel}</Button>
                    </Form>
                </div>)
        }
}

module.exports = CreateEvent;
