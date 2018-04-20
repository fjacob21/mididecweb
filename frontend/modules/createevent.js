import React from 'react'
import jquery from 'jquery'
import { Button, Form, FormGroup, Label, Input, Alert } from 'reactstrap';

class CreateEvent extends React.Component{
        constructor(props) {
            super(props);
            this.state = {
                  valid: false,
                  alert: {
                          visible: false,
                          message: '',
                          color: 'success'
                      },
                  values: { title: '',
                      desc: '',
                      maxAttendee: '20',
                      startDate: '',
                      time: '12:00',
                      durationString: '1h00',
                      location: '3b6',
                      organizerName: 'Frederic Jacob',
                      organizerEmail: 'fjacob@matrox.com'}
            };
            this.onCancel = this.onCancel.bind(this);
            this.onAdd = this.onAdd.bind(this);
            this.onChange = this.onChange.bind(this);
            this.addSuccess = this.addSuccess.bind(this);
            this.addError = this.addError.bind(this);
            this.onDismiss = this.onDismiss.bind(this);
        }

        onDismiss() {
                this.state.alert.visible = false;
                this.setState(this.state);
        }

        addSuccess(data){
            this.showAlert('l\'evenement a ete enregistre', 'success')
        }

        addError(data){
                this.showAlert('Une erreur est survenue lors de la create de l\'evenement!', 'danger')
        }

        showAlert(message, color='success'){
                this.state.alert.color = color;
                this.state.alert.visible = true;
                this.state.alert.message = message;
                this.setState(this.state);
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
            this.state.values.start = this.parseDate(this.state.values.startDate, this.state.values.time);
            this.state.values.duration = this.parseDuration(this.state.values.durationString);
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

        }

        onChange(e) {
                this.state.values[e.target.id] = e.target.value;
                if (this.title != '' && this.desc != '')
                        this.state.valid = true;
                this.setState(this.state);
        }

        render() {
            return (
                <div className='createevent'>
                    <Alert color={this.state.alert.color} isOpen={this.state.alert.visible} toggle={this.onDismiss}>
                            {this.state.alert.message}
                    </Alert>
                    <Form className='form'>
                            <FormGroup className='title'>
                                    <Label for="title">Titre <font size="3" color="red">*</font></Label>
                                    <Input onChange={this.onChange} type='text' name="title" id="title" placeholder="title" value={this.state.values.title} />
                            </FormGroup>
                            <FormGroup className='desc'>
                                    <Label for="desc">Description <font size="3" color="red">*</font></Label>
                                    <Input onChange={this.onChange} type='textarea' name="desc" id="desc" placeholder="desc" value={this.state.values.description} />
                            </FormGroup>
                            <FormGroup className='maxAttendee'>
                                    <Label for="maxAttendee">maxAttendee</Label>
                                    <Input onChange={this.onChange} type='text' name="maxAttendee" id="maxAttendee" placeholder="20" value={this.state.values.maxAttendee} />
                            </FormGroup>
                            <FormGroup className='startDate'>
                                    <Label for="startDate">Start</Label>
                                    <div><Input onChange={this.onChange} type='date' name="startDate" id="startDate" placeholder="startDate" value={this.state.values.startDate} />
                                    <Input onChange={this.onChange} type='time' name="time" id="time" placeholder="time" value={this.state.values.time} /></div>
                            </FormGroup>
                            <FormGroup className='durationString'>
                                    <Label for="durationString">Duration </Label>
                                    <Input onChange={this.onChange} type='text' name="durationString" id="durationString" placeholder="durationString" value={this.state.values.durationString} />
                            </FormGroup>
                            <FormGroup className='location'>
                                    <Label for="location">location</Label>
                                    <Input onChange={this.onChange} type='text' name="location" id="location" placeholder="location" value={this.state.values.location} />
                            </FormGroup>
                            <FormGroup className='organizerName'>
                                    <Label for="organizerName">organizerName</Label>
                                    <Input onChange={this.onChange} type='text' name="organizerName" id="organizerName" placeholder="organizerName" value={this.state.values.organizerName} />
                            </FormGroup>
                            <FormGroup className='organizerEmail'>
                                    <Label for="title">organizerEmail</Label>
                                    <Input onChange={this.onChange} type='email' name="organizerEmail" id="organizerEmail" placeholder="organizerEmail" value={this.state.values.organizerEmail} />
                            </FormGroup>
                            <Button color="primary" onClick={this.onAdd} disabled={!this.state.valid}>Ajouter</Button>{' '}
                            <Button color="secondary" onClick={this.onCancel}>Cancel</Button>
                    </Form>
                </div>)
        }
}

module.exports = CreateEvent;
