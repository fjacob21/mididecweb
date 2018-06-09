import React , { Component, PropTypes } from 'react'
import { browserHistory} from 'react-router'
import jquery from 'jquery'
import createHistory from "history/createHashHistory"
import User from './user'
import Errors from './errors'
import FormQuery from './formquery'
import { Button, Form, FormGroup, Label, Input, Card, CardTitle, FormFeedback, UncontrolledTooltip } from 'reactstrap';
import {isValidNumber} from 'libphonenumber-js'
import Text from './localization/text'

const history = createHistory();

Text.getLocales();
class CreateUser extends React.Component{
        constructor(props) {
                super(props);
                this.state = {
                      valid: false,
                      localValidation: {
                              nameok: true,
                              emailok: true,
                              aliasok: true,
                              passwordok: true,
                              phoneok:true
                      },
                      validation: {
                              emailok: true,
                              aliasok: true
                      },
                      tooltipOpen: false,
                      values: { name: '',
                                email: '',
                                password: '',
                                alias: '',
                                phone: '',
                                useemail: true,
                                usesms: false
                        }
                };
                this.onCreate = this.onCreate.bind(this);
                this.createSuccess = this.createSuccess.bind(this);
                this.createError = this.createError.bind(this);
                this.validateSuccess = this.validateSuccess.bind(this);
                this.validateError = this.validateError.bind(this);
                this.onChange = this.onChange.bind(this);
                this.onBlur = this.onBlur.bind(this);
                this.onCheck = this.onCheck.bind(this);
                this.onKeyPress = this.onKeyPress.bind(this);
                this.toggle = this.toggle.bind(this);
                this.enter = this.enter.bind(this);
        }

        componentDidMount(){
        }

        componentWillUnmount(){
        }

        onCheck(e){
                this.state.values[e.target.id] = e.target.checked;
                this.updateLocalValidation();
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
                this.updateLocalValidation();
                this.setState(this.state);
        }

        onBlur(e){
            if (FormQuery.isIos()) {
                    var fq = new FormQuery(this.state.values);
                    this.state.values = fq.parse();
                    this.validateUser();
                    this.updateLocalValidation();
                    this.setState(this.state);
            }
            else {
                    this.updateLocalValidation(e.target.id);
                    this.setState(this.state);
            }
        }

        onKeyPress(e){
                if (e.key == 'Enter' && this.state.valid)
                        this.onCreate();
        }

        updateLocalValidation(target){
                if (target == 'name' || !target){
                        this.state.localValidation.nameok = true;
                        if (!this.state.values.name)
                                this.state.localValidation.nameok = false;
                }
                if (target == 'email' || !target){
                        this.state.localValidation.emailok = true;
                        if (!this.state.values.email)
                                this.state.localValidation.emailok = false;
                }
                if (target == 'alias' || !target) {
                        this.state.localValidation.aliasok = true;
                        if (!this.state.values.alias)
                                this.state.localValidation.aliasok = false;
                }
                if (target == 'password' || !target) {
                        this.state.localValidation.passwordok = true;
                        if (!this.state.values.password)
                                this.state.localValidation.passwordok = false;
                }
                this.state.localValidation.phoneok = true;
                if (this.state.values.phone && !this.isPhoneValid(this.state.values.phone))
                        this.state.localValidation.phoneok = false;
                this.setState(this.state);
        }

        validateUser(){
                jquery.ajax({
                type: 'POST',
                url: "/mididec/api/v1.0/users/validate",
                data: JSON.stringify (this.state.values),
                success: this.validateSuccess,
                error: this.validateError,
                contentType: "application/json",
                dataType: 'json'
                });
        }

        validateSuccess(data){
                this.state.valid = false;
                this.state.validation = data;
                if (data.emailok && data.aliasok) {
                    var at = this.state.values.email.indexOf('@');
                    var dot = this.state.values.email.lastIndexOf('.');
                    if (this.state.values.name != '' &&
                        this.state.values.email != '' &&
                        this.state.values.password != '' &&
                        this.state.values.alias != '' &&
                        at != -1 && dot != -1 && at < dot &&
                        (dot+1) < this.state.values.email.length&&
                        (!this.state.values.phone || this.isPhoneValid(this.state.values.phone))) {
                            this.state.valid = true;
                    }
                }
                this.setState(this.state);
        }

        validateError(data){

        }

        onCreate() {
            this.state.valid = false;
            this.setState(this.state);
            jquery.ajax({
            type: 'POST',
            url: "/mididec/api/v1.0/users",
            data: JSON.stringify (this.state.values),
            success: this.createSuccess,
            error: this.createError,
            contentType: "application/json",
            dataType: 'json'
            });
        }

        createSuccess(data){
            history.replace("/login");
        }

        createError(data){
            var errorCode = data.responseJSON.code;
            this.showAlert(Errors.getErrorMessage(errorCode), 'danger');
        }

        showAlert(message, color='success'){
                this.props.onError(message, color);
        }

        isPhoneValid(phone){
            return isValidNumber(phone, 'CA');
        }

        enter() {
                this.updateLocalValidation();
        }

        toggle() {
                console.debug('toggle');
                this.state.tooltipOpen = !this.state.tooltipOpen;
                this.setState(this.state);
        }
        render(){
                var emailErrorMessage = <div className='empty'>e</div>;
                if (!this.state.localValidation.emailok)
                        emailErrorMessage = <FormFeedback>{Text.text.user_empty_email}</FormFeedback>
                if (!this.state.validation.emailok)
                        emailErrorMessage = <FormFeedback>{Text.text.user_invalid_email}</FormFeedback>
                var aliasErrorMessage = <div className='empty'>e</div>;
                if (!this.state.localValidation.aliasok)
                        aliasErrorMessage = <FormFeedback>{Text.text.user_empty_alias}</FormFeedback>
                if (!this.state.validation.aliasok)
                        aliasErrorMessage = <FormFeedback>{Text.text.user_invalid_alias}</FormFeedback>
                var nameErrorMessage = <div className='empty'>e</div>;
                if (!this.state.localValidation.nameok)
                        nameErrorMessage = <FormFeedback>{Text.text.user_empty_name}</FormFeedback>
                var passwordErrorMessage = <div className='empty'>e</div>;
                if (!this.state.localValidation.passwordok)
                        passwordErrorMessage = <FormFeedback>{Text.text.user_empty_password}</FormFeedback>
                var phoneErrorMessage = <div className='empty'>e</div>;
                if (!this.state.localValidation.phoneok)
                        phoneErrorMessage = <FormFeedback>{Text.text.user_invalid_phone}</FormFeedback>
                return (
                        <div className='createuser'>
                                <Card body className='createuser-card'>
                                        <CardTitle>{Text.text.user_add_title}</CardTitle>

                                        <Form className='createuser-form' onKeyPress={this.onKeyPress}>
                                                <FormGroup className='name'>
                                                        <Label for="name">{Text.text.name} <font size="3" color="red">*</font></Label>
                                                        <div>
                                                                <Input onBlur={this.onBlur} invalid={!this.state.localValidation.nameok} onChange={this.onChange} autoComplete='name' type='text' name="name" id="name" placeholder="Nom" value={this.state.values.name} />
                                                                {nameErrorMessage}
                                                        </div>
                                                </FormGroup>
                                                <FormGroup className='email'>
                                                        <Label for="email">{Text.text.user_email_label} <font size="3" color="red">*</font></Label>
                                                        <div>
                                                                <Input onBlur={this.onBlur} invalid={!this.state.validation.emailok||!this.state.localValidation.emailok} autoComplete='email' onChange={this.onChange} type='email' name="email" id="email" placeholder="test@test.com" value={this.state.values.email} />
                                                                {emailErrorMessage}
                                                        </div>
                                                </FormGroup>
                                                <FormGroup className='alias'>
                                                        <Label for="alias">{Text.text.user_alias_label} <font size="3" color="red">*</font></Label>
                                                        <div>
                                                                <Input onBlur={this.onBlur} invalid={!this.state.validation.aliasok||!this.state.localValidation.aliasok} autoComplete='alias' onChange={this.onChange} type='text' name="alias" id="alias" placeholder="alias" value={this.state.values.alias} />
                                                                {aliasErrorMessage}
                                                        </div>
                                                </FormGroup>
                                                <FormGroup className='password'>
                                                        <Label for="password">{Text.text.password} <font size="3" color="red">*</font></Label>
                                                        <div>
                                                                <Input onBlur={this.onBlur} invalid={!this.state.localValidation.passwordok} onChange={this.onChange} autoComplete='current-password' type='password' name="password" id="password" value={this.state.values.password} />
                                                                {passwordErrorMessage}
                                                        </div>
                                                </FormGroup>
                                                <FormGroup className='phone'>
                                                        <Label for="phone">{Text.text.user_phone_label}</Label>
                                                        <div>
                                                                <Input onBlur={this.onBlur} invalid={!this.state.localValidation.phoneok} onChange={this.onChange} autoComplete='tel' type='text' name="phone" id="phone" placeholder="+15551234567" value={this.state.values.phone} />
                                                                {phoneErrorMessage}

                                                        </div>
                                                </FormGroup>
                                                <FormGroup check  className='use'>
                                                        <Label>
                                                                <Input onBlur={this.onBlur} onChange={this.onCheck} type='checkbox' id="useemail" checked={this.state.values.useemail} />
                                                                {Text.text.user_useemail_label}
                                                        </Label>
                                                </FormGroup>
                                                <FormGroup check>
                                                        <Label>
                                                                <Input onBlur={this.onBlur} onChange={this.onCheck} type='checkbox' id="usesms" checked={this.state.values.usesms} />
                                                                {Text.text.user_usesms_label}
                                                        </Label>
                                                </FormGroup>
                                                <div>
                                                <Button color="primary"  id='btadd' onMouseEnter={this.enter} onClick={this.onCreate} disabled={!this.state.valid}>{Text.text.user_add_add_label}</Button>{' '}
                                                </div>
                                        </Form>
                                </Card>
                        </div>)
        }
}

module.exports = CreateUser;
