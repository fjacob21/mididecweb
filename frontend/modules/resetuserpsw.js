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

class ResetUserPsw extends React.Component{
        constructor(props) {
                super(props);
                this.state = {
                      valid: false,
                      values: { password: ''}
                };
                this.getUser();
                // this.onCancel = this.onCancel.bind(this);
                // this.onUpdate = this.onUpdate.bind(this);
                // this.updateSuccess = this.updateSuccess.bind(this);
                // this.updateError = this.updateError.bind(this);
                // this.validateSuccess = this.validateSuccess.bind(this);
                // this.validateError = this.validateError.bind(this);
                // this.onChange = this.onChange.bind(this);
                // this.onBlur = this.onBlur.bind(this);
                // this.onCheck = this.onCheck.bind(this);
                // this.onKeyPress = this.onKeyPress.bind(this);
                // this.handleFileUpload = this.handleFileUpload.bind(this);
                // this.onFile = this.onFile.bind(this);
                // this.onSendCode = this.onSendCode.bind(this);
                // this.sendCodeSuccess = this.sendCodeSuccess.bind(this);
                // this.sendCodeError = this.sendCodeError.bind(this);
                // this.onValidateCode = this.onValidateCode.bind(this);
                // this.validateCodeSuccess = this.validateCodeSuccess.bind(this);
                // this.validateCodeError = this.validateCodeError.bind(this);

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
                console.debug('seccess');
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

        render(){
                var user = User.getSession();
                return (
                        <div className='updateuser'>
                                <Card body className='updateuser-card'>
                                        <CardTitle>{Text.text.profile}</CardTitle>

                                        <Form className='updateuser-form' onKeyPress={this.onKeyPress}>
                                                <FormGroup className='password'>
                                                        <Label for="password">{Text.text.password}</Label>
                                                        <Input onBlur={this.onBlur} onChange={this.onChange} autoComplete='current-password' type='password' name="password" id="password" value={this.state.values.password} />
                                                </FormGroup>
                                                <Button className='bt-update' color="primary" onClick={this.onUpdate} disabled={!this.state.valid}>{Text.text.save}</Button>
                                                <Button color="secondary" onClick={this.onCancel} >{Text.text.cancel}</Button>
                                        </Form>
                                </Card>
                        </div>)
        }
}

module.exports = ResetUserPsw;
