import React , { Component, PropTypes } from 'react'
import { browserHistory} from 'react-router'
import jquery from 'jquery'
import createHistory from "history/createHashHistory"
import User from './user'
import Errors from './errors'
import FormQuery from './formquery'
import { Button, Form, FormGroup, Label, Input, Card, CardTitle, FormFeedback } from 'reactstrap';
import {isValidNumber} from 'libphonenumber-js'
import Text from './localization/text'

const history = createHistory();

class UpdateUser extends React.Component{
        constructor(props) {
                super(props);
                this.state = {
                      valid: false,
                      validation: {
                              emailok: true,
                              aliasok: true
                      },
                      values: { name: '',
                                email: '',
                                password: '',
                                alias: '',
                                phone: '',
                                useemail: true,
                                usesms: false,
                                profile: '',
                                access: 0,
                                smscode: ''
                        }
                };
                this.getUser();
                this.onCancel = this.onCancel.bind(this);
                this.onUpdate = this.onUpdate.bind(this);
                this.updateSuccess = this.updateSuccess.bind(this);
                this.updateError = this.updateError.bind(this);
                this.validateSuccess = this.validateSuccess.bind(this);
                this.validateError = this.validateError.bind(this);
                this.onChange = this.onChange.bind(this);
                this.onBlur = this.onBlur.bind(this);
                this.onCheck = this.onCheck.bind(this);
                this.onKeyPress = this.onKeyPress.bind(this);
                this.handleFileUpload = this.handleFileUpload.bind(this);
                this.onFile = this.onFile.bind(this);
                this.onSendCode = this.onSendCode.bind(this);
                this.sendCodeSuccess = this.sendCodeSuccess.bind(this);
                this.sendCodeError = this.sendCodeError.bind(this);
                this.onValidateCode = this.onValidateCode.bind(this);
                this.validateCodeSuccess = this.validateCodeSuccess.bind(this);
                this.validateCodeError = this.validateCodeError.bind(this);

        }

        getUser(){
                var user = User.getSession();
                jquery.ajax({
                type: 'GET',
                url: "/mididec/api/v1.0/users/"+ this.props.match.params.id+'?loginkey='+user.loginkey,
                success: this.success.bind(this),
                error: this.error.bind(this),
                contentType: "application/json",
                dataType: 'json'
                });
        }

        componentDidMount(){
        }

        componentWillUnmount(){
        }

        success(data){
                this.state.values = data.user;
                this.state.values.smscode = '';
                this.state.values.password = '';
                this.state.invalid = false;
                this.setState(this.state);
        }

        error(data){
            var errorCode = data.responseJSON.code;
            this.showAlert(Errors.getErrorMessage(errorCode), 'danger');
        }

        onCancel(e) {
                history.goBack();
        }

        onCheck(e){
                this.state.values[e.target.id] = e.target.checked;
                this.validateUser();
                this.setState(this.state);
        }

        onChange(e) {
                if (FormQuery.isIos()) {
                        var fq = new FormQuery(this.state.values);
                        this.state.values = fq.parse();
                }
                else {
                        this.state.values[e.target.id] = e.target.value;
                }
                this.validateUser();
                this.setState(this.state);
        }

        onBlur(e){
            if (FormQuery.isIos()) {
                    var fq = new FormQuery(this.state.values);
                    this.state.values = fq.parse();
                    this.validateUser();
                    this.setState(this.state);
            }
        }

        onKeyPress(e){
                if (e.key == 'Enter' && this.state.valid)
                        this.onUpdate();
        }

        validateUser(){
                var user = User.getSession();
                jquery.ajax({
                type: 'POST',
                url: "/mididec/api/v1.0/users/validate?loginkey=" + user.loginkey,
                data: JSON.stringify (this.state.values),
                success: this.validateSuccess,
                error: this.validateError,
                contentType: "application/json",
                dataType: 'json'
                });
        }

        validateSuccess(data){
                this.state.validation = data;
                this.state.valid = false;
                if (data.emailok && data.aliasok) {
                    var at = this.state.values.email.indexOf('@');
                    var dot = this.state.values.email.lastIndexOf('.');
                    if (this.state.values.name != '' &&
                        this.state.values.email != '' &&
                        this.state.values.alias != '' &&
                        at != -1 && dot != -1 && at < dot &&
                        (dot+1) < this.state.values.email.length &&
                        (!this.state.values.phone || this.isPhoneValid(this.state.values.phone)))
                            this.state.valid = true;
                }
                this.setState(this.state);
        }

        validateError(data){
            var errorCode = data.responseJSON.code;
            this.showAlert(Errors.getErrorMessage(errorCode), 'danger');
        }

        onUpdate() {
            this.props.onloading(true);
            var user = User.getSession();
            this.state.values.loginkey = user.loginkey;
            this.state.valid = false;
            this.setState(this.state);
            jquery.ajax({
            type: 'POST',
            url: "/mididec/api/v1.0/users/" + this.props.match.params.id,
            data: JSON.stringify (this.state.values),
            success: this.updateSuccess,
            error: this.updateError,
            contentType: "application/json",
            dataType: 'json'
            });
        }

        updateSuccess(data){
            this.props.onloading(false);
            this.showAlert(Text.text.update_success, 'success');
            this.getUser();
        }

        updateError(data){
            this.props.onloading(false);
            var errorCode = data.responseJSON.code;
            this.showAlert(Errors.getErrorMessage(errorCode), 'danger');
        }

        showAlert(message, color='success'){
                this.props.onError(message, color);
        }

        handleFileUpload(event){
            this.props.onloading(true);
            var user = User.getSession();
            const file = event.target.files[0];
            const formData = new FormData()
            formData.append('avatar', file, file.name);
            jquery.ajax({
            type: 'POST',
            url: "/mididec/api/v1.0/users/" + this.props.match.params.id+"/avatar?loginkey="+user.loginkey,
            data: formData,
            processData: false,
            contentType: false,
            success: this.updateSuccess,
            error: this.updateError
            });
        }

        onFile(){
                document.getElementById('profile_pic').click();
        }

        onSendCode(){
            this.props.onloading(true);
            var user = User.getSession();
            this.state.values.loginkey = user.loginkey;
            this.setState(this.state);
            jquery.ajax({
            type: 'POST',
            url: "/mididec/api/v1.0/users/" + this.props.match.params.id + "/sendcode",
            data: JSON.stringify (this.state.values),
            success: this.sendCodeSuccess,
            error: this.sendCodeError,
            contentType: "application/json",
            dataType: 'json'
            });
        }

        sendCodeSuccess(data){
            this.props.onloading(false);
            this.showAlert(Text.text.sms_code_send_success, 'success');
            this.getUser();
        }

        sendCodeError(data){
            this.props.onloading(false);
            var errorCode = data.responseJSON.code;
            this.showAlert(Errors.getErrorMessage(errorCode), 'danger');
        }

        onValidateCode(){
            this.props.onloading(true);
            var user = User.getSession();
            this.state.values.loginkey = user.loginkey;
            this.setState(this.state);
            jquery.ajax({
            type: 'POST',
            url: "/mididec/api/v1.0/users/" + this.props.match.params.id + "/validatecode",
            data: JSON.stringify (this.state.values),
            success: this.validateCodeSuccess,
            error: this.validateCodeError,
            contentType: "application/json",
            dataType: 'json'
            });
        }

        validateCodeSuccess(data){
            this.props.onloading(false);
            this.showAlert(Text.text.phone_validated_msg, 'success');
            this.getUser();
        }

        validateCodeError(data){
            this.props.onloading(false);
            var errorCode = data.responseJSON.code;
            this.showAlert(Errors.getErrorMessage(errorCode), 'danger');
        }

        isPhoneValid(phone){
            return isValidNumber(phone, 'CA');
        }

        render(){
                var user = User.getSession();
                var access = "";
                if (user.isSuperUser)
                        access = (<FormGroup className='profile'>
                                <Label for="access">{Text.text.access}</Label>
                                <div>
                                        <Input type="select" name="access" id="access" onChange={this.onChange} value={this.state.values.access.toString()}>
                                            <option value='0'>{Text.text.normal_access}</option>
                                            <option value='3'>{Text.text.manager_access}</option>
                                            <option value='255'>{Text.text.super_access}</option>
                                        </Input>
                                </div>
                        </FormGroup>);
                var emailErrorMessage = "";
                if (!this.state.validation.emailok)
                        emailErrorMessage = <FormFeedback>{Text.text.email_already_used_msg}</FormFeedback>
                var aliasErrorMessage = "";
                if (!this.state.validation.aliasok)
                        aliasErrorMessage = <FormFeedback>{Text.text.alias_already_used_msg}</FormFeedback>
                var avatar = <i className="material-icons md-light attendee-avatar-default">account_circle</i>
                if (this.state.values.have_avatar) {
                        var avatar_path = "/mididec/api/v1.0/users/" + this.props.match.params.id+"/avatar?sizex=100&sizey=110&id=" + new Date().getTime();
                        avatar = <img src={avatar_path} className="attendee-icon"/>
                }
                var smsvalidation = "";
                if (!this.state.values.smsvalidated && this.state.values.phone && this.isPhoneValid(this.state.values.phone)) {
                    smsvalidation = (<div className='smsvalidation'>
                                        <Label for="smscode">{Text.text.validation_code}</Label>
                                        <div className='smsinput'>
                                            <Input className='smscode' onChange={this.onChange} type='text' name="smscode" id="smscode" value={this.state.values.smscode} />
                                            <Button color='success' className='smvalidatebt' onClick={this.onValidateCode}>{Text.text.validation}</Button>
                                            <Button color='warning' className='smssendbt' onClick={this.onSendCode}>{Text.text.send_code}</Button>
                                        </div>
                                    </div>);
                }
                return (
                        <div className='updateuser'>
                                <Card body className='updateuser-card'>
                                        <CardTitle>{Text.text.profile}</CardTitle>

                                        <Form className='updateuser-form' onKeyPress={this.onKeyPress}>
                                                {avatar}
                                                <FormGroup className='name'>
                                                        <Button onClick={this.onFile}>{Text.text.change_avatar}</Button>
                                                        <Input onBlur={this.onBlur} className="file" type="file" id="profile_pic" name="profile_pic" onChange={this.handleFileUpload} accept="image/*"/>
                                                </FormGroup>
                                                <FormGroup className='name'>
                                                        <Label for="name">{Text.text.name} <font size="3" color="red">*</font></Label>
                                                        <Input onBlur={this.onBlur} onChange={this.onChange} autoComplete='name' type='text' name="name" id="name" placeholder="Nom" value={this.state.values.name} />
                                                </FormGroup>
                                                <FormGroup className='email'>
                                                        <Label for="email">{Text.text.user_email_label} <font size="3" color="red">*</font></Label>
                                                        <div>
                                                                <Input onBlur={this.onBlur} invalid={!this.state.validation.emailok} autoComplete='email' onChange={this.onChange} type='email' name="email" id="email" placeholder="test@test.com" value={this.state.values.email} />
                                                                {emailErrorMessage}
                                                        </div>
                                                </FormGroup>
                                                <FormGroup className='alias'>
                                                        <Label for="alias">{Text.text.user_alias_label} <font size="3" color="red">*</font></Label>
                                                        <div>
                                                                <Input onBlur={this.onBlur} invalid={!this.state.validation.aliasok} autoComplete='alias' onChange={this.onChange} type='text' name="alias" id="alias" placeholder="alias" value={this.state.values.alias} />
                                                                {aliasErrorMessage}
                                                        </div>
                                                </FormGroup>
                                                <FormGroup className='password'>
                                                        <Label for="password">{Text.text.password}</Label>
                                                        <Input onBlur={this.onBlur} onChange={this.onChange} autoComplete='current-password' type='password' name="password" id="password" value={this.state.values.password} />
                                                </FormGroup>
                                                <FormGroup className='phone'>
                                                        <div className='phone-input'>
                                                            <Label for="phone">{Text.text.user_phone_label}</Label>
                                                            <Input onBlur={this.onBlur} onChange={this.onChange} autoComplete='tel' type='text' name="phone" id="phone" placeholder="+15551234567" value={this.state.values.phone} />
                                                        </div>
                                                        {smsvalidation}

                                                </FormGroup>
                                                <FormGroup className='profile'>
                                                        <Label for="profile">{Text.text.profile}</Label>
                                                        <div>
                                                                <Input onBlur={this.onBlur} autoComplete='profile' onChange={this.onChange} type='text' name="profile" id="profile" placeholder="profile" value={this.state.values.profile} />
                                                        </div>
                                                </FormGroup>
                                                {access}
                                                <FormGroup check>
                                                        <Label>
                                                                <Input onBlur={this.onBlur} onChange={this.onCheck} type='checkbox' id="useemail" checked={this.state.values.useemail} />{' '}
                                                                {Text.text.user_useemail_label}
                                                        </Label>
                                                </FormGroup>
                                                <FormGroup check>
                                                        <Label>
                                                                <Input onBlur={this.onBlur} onChange={this.onCheck} type='checkbox' id="usesms" checked={this.state.values.usesms} />
                                                                {Text.text.user_usesms_label}
                                                        </Label>
                                                </FormGroup>
                                                <Button className='bt-update' color="primary" onClick={this.onUpdate} disabled={!this.state.valid}>{Text.text.save}</Button>
                                                <Button color="secondary" onClick={this.onCancel} >{Text.text.cancel}</Button>
                                        </Form>
                                </Card>
                        </div>)
        }
}

module.exports = UpdateUser;
