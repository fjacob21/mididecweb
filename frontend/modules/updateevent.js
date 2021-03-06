import React from 'react'
import jquery from 'jquery'
import User from './user'
import createHistory from "history/createHashHistory"
import Errors from './errors'
import FormQuery from './formquery'
import { Button, Form, FormGroup, Label, Input, Modal, ModalHeader, ModalBody, ModalFooter, FormFeedback  } from 'reactstrap';
import Text from './localization/text'
import AttachmentSummary from './attachmentsummary'

const history = createHistory();

class UpdateEvent extends React.Component{
        constructor(props) {
            super(props);
            var user = User.getSession();
            this.state = {
                  modal: false,
                  valid: false,
                  localValidation: {
                          max_attendee: true
                  },
                  values: { title: '',
                      description: '',
                      max_attendee: '20',
                      startDate: '',
                      time: '12:00',
                      durationString: '1h00',
                      location: '3b6',
                      organizer_name: user.alias,
                      organizer_email: user.email,
                      not_training: false,
                      attachments: []}
            };
            var user = User.getSession();
            this.getEvent();
            this.onCancel = this.onCancel.bind(this);
            this.onUpdate = this.onUpdate.bind(this);
            this.onChange = this.onChange.bind(this);
            this.updateSuccess = this.updateSuccess.bind(this);
            this.updateError = this.updateError.bind(this);
            this.handleFileUpload = this.handleFileUpload.bind(this);
            this.onFile = this.onFile.bind(this);
            this.onPresences = this.onPresences.bind(this);
            this.onPublish = this.onPublish.bind(this);
            this.publishSuccess = this.publishSuccess.bind(this);
            this.publishError = this.publishError.bind(this);
            this.onKeyPress = this.onKeyPress.bind(this);
            this.onBlur = this.onBlur.bind(this);
            this.onAttachmentDelete = this.onAttachmentDelete.bind(this);
            this.rmSuccess = this.rmSuccess.bind(this);
            this.rmError = this.rmError.bind(this);
            this.onAccept = this.onAccept.bind(this);
            this.onRefuse = this.onRefuse.bind(this);
            this.onCheck = this.onCheck.bind(this);
        }

        getEvent(){
                var user = User.getSession();
                jquery.ajax({
                type: 'GET',
                url: "/mididec/api/v1.0/events/"+ this.props.match.params.id+'?loginkey='+user.loginkey,
                success: this.success.bind(this),
                error: this.error.bind(this),
                contentType: "application/json",
                dataType: 'json'
                });
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
            this.props.onloading(false);
            this.showAlert(Text.text.event_add_success, 'success')
            this.getEvent();
        }

        updateError(data){
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

        onUpdate() {
            this.props.onloading(true);
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

        onCheck(e){
                this.state.values[e.target.id] = e.target.checked;
                var n = new Date(Date.now());
                var start = new Date(this.state.values.startDate + "T" + this.state.values.time + 'Z');
                start = new Date(start.setTime( start.getTime() + start.getTimezoneOffset()*60*1000 ));
                var isBefore = n > start;
                if (this.state.values.title != '' && this.state.values.description != '' && this.state.values.startDate != '' && !isBefore)
                        this.state.valid = true;
                this.setState(this.state);
        }

        onPresences() {
                history.replace("/events/"+this.props.match.params.id+"/presence");
        }

        onPdf() {
            var presencesurl = '/mididec/api/v1.0/events/' + this.props.event.event_id + '/presences';
            history.replace(presencesurl);
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
            this.showAlert(Text.text.event_published, 'success')
        }

        publishError(data){
            var errorCode = data.responseJSON.code;
            this.showAlert(Errors.getErrorMessage(errorCode), 'danger');
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
                this.updateLocalValidation();
                this.setState(this.state);
        }

        handleFileUpload(event){

                this.props.onloading(true);
                var user = User.getSession();
                const file = event.target.files[0];
                if (file == undefined) {
                  this.props.onloading(false);
                  return;
                }
                const formData = new FormData()
                console.debug(event, file);
                formData.append('attachment', file, file.name);
                jquery.ajax({
                type: 'POST',
                url: "/mididec/api/v1.0/events/" + this.props.match.params.id+"/attachments?loginkey="+user.loginkey,
                data: formData,
                processData: false,
                contentType: false,
                success: this.updateSuccess,
                error: this.updateError
                });
        }

        onFile(){
                document.getElementById('add_attachment').click();
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
            else {
                    this.updateLocalValidation(e.target.id);
                    this.setState(this.state);
            }
        }

        onKeyPress(e){
                if (e.key == 'Enter' && this.state.valid)
                        this.onAdd();
        }

        updateLocalValidation(target){
                if (target == 'max_attendee' || !target){
                        this.state.localValidation.max_attendee = true;
                        if (this.state.values.attendees.length > parseInt(this.state.values.max_attendee, 10)) {
                                this.state.localValidation.max_attendee = false;
                                this.state.valid = false;
                        }
                }
                this.setState(this.state);
        }

        onAttachmentDelete(attachment){
                this.state.modal = true;
                this.state.modalAttachment = attachment;
                this.setState(this.state);
        }

        rmSuccess(data){
                this.showAlert(Text.text.user_delete_success, 'success');
                this.getEvent();
        }

        rmError(data){
                var errorCode = data.responseJSON.code;
                this.showAlert(Errors.getErrorMessage(errorCode), 'danger');
        }

        onAccept(){
                var user = User.getSession();
                jquery.ajax({
                type: 'DELETE',
                url: "/mididec/api/v1.0/events/"+this.props.match.params.id+"/attachments",
                data: JSON.stringify ({loginkey: user.loginkey, attachment:this.state.modalAttachment}),
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
                this.state.modalAttachment = null;
                this.setState(this.state);
        }

        render() {
            var attachments = '';
            attachments = this.state.values.attachments.map((attachment) =>
                    <AttachmentSummary key={attachment} attachment={attachment} onDelete={this.onAttachmentDelete}> {attachment} </AttachmentSummary>
            );
            var modalTitle = "";
            if (this.state.modalAttachment)
                    modalTitle = this.state.modalAttachment;
            var maxAttendeeErrorMessage = <div className='empty'>e</div>;
            if (!this.state.localValidation.max_attendee)
                    maxAttendeeErrorMessage = <FormFeedback>{Text.text.err_attendee_too_low_msg}</FormFeedback>
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
                                    <Label for="max_attendee">{Text.text.event_max_attendee_label} </Label>
                                    <Input onBlur={this.onBlur} onChange={this.onChange} invalid={!this.state.localValidation.max_attendee} type='text' name="max_attendee" id="max_attendee" placeholder="20" value={this.state.values.max_attendee} />
                                    {maxAttendeeErrorMessage}
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
                            <FormGroup className='add_attachment'>
                                        <Label>{Text.text.event_attachments_label}</Label>
                                        {attachments}
                                        <Button onClick={this.onFile}>{Text.text.add_attachment}</Button>
                                        <Input onBlur={this.onBlur} className="file" type="file" id="add_attachment" name="add_attachment" onChange={this.handleFileUpload} accept="*"/>
                            </FormGroup>
                            <Button color="primary" onClick={this.onUpdate} disabled={!this.state.valid}>{Text.text.save}</Button>{' '}
                            <Button color="secondary" onClick={this.onCancel}>{Text.text.cancel}</Button>{' '}
                            <Button color="warning" onClick={this.onPublish}>{Text.text.publish}</Button>{' '}
                            <Button color="warning" onClick={this.onPresences}>{Text.text.presences}</Button>
                    </Form>
                    <Modal isOpen={this.state.modal}>
                            <ModalHeader toggle={this.toggle}>{modalTitle}</ModalHeader>
                            <ModalBody>
                                    {Text.text.attachment_delete_confirmation}
                            </ModalBody>
                            <ModalFooter>
                                    <Button color="primary" onClick={this.onAccept}>{Text.text.yes}</Button>{' '}
                                    <Button color="secondary" onClick={this.onRefuse}>{Text.text.no}</Button>
                            </ModalFooter>
                    </Modal>
                </div>)
        }
}

module.exports = UpdateEvent;
