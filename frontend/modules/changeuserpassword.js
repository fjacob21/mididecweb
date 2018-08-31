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

class ChangeUserPassword extends React.Component{
        constructor(props) {
                super(props);
                var request_id = this.props.match.params.reqid;
                this.state = { valid: false,
                      values: { request_id: request_id, password: ''}
                };
                jquery.ajax({
                type: 'POST',
                url: "/mididec/api/v1.0/users/resetpsw/validate",
                data: JSON.stringify (this.state.values),
                success: this.success.bind(this),
                error: this.error.bind(this),
                contentType: "application/json",
                dataType: 'json'
                });
                this.onChangePassword = this.onChangePassword.bind(this);
                this.changePasswordSuccess = this.changePasswordSuccess.bind(this);
                this.changePasswordError = this.changePasswordError.bind(this);
                this.onChange = this.onChange.bind(this);
                this.onBlur = this.onBlur.bind(this);
                this.onKeyPress = this.onKeyPress.bind(this);
        }

        success(data){
                this.state.valid = data.result;
                if (!this.state.valid)
                  this.showAlert(Text.text.invalid_request_msg, 'danger');
                this.setState(this.state);
        }

        error(data){
                var errorCode = data.responseJSON.code;
                this.showAlert(Errors.getErrorMessage(errorCode), 'danger');
        }

        componentDidMount(){
        }

        componentWillUnmount(){
        }

        onChange(e) {
                if (FormQuery.isIos()) {
                        var fq = new FormQuery(this.state.values);
                        this.state.values = fq.parse();
                }
                else {
                        this.state.values[e.target.id] = e.target.value;
                }
                this.setState(this.state);
        }

        onBlur(e){
            if (FormQuery.isIos()) {
                    var fq = new FormQuery(this.state.values);
                    this.state.values = fq.parse();
                    this.setState(this.state);
            }
        }

        onKeyPress(e){
                if (e.key == 'Enter')
                        this.onChangePassword();
        }

        onChangePassword() {
            this.props.onloading(true);
            jquery.ajax({
            type: 'POST',
            url: "/mididec/api/v1.0/users/resetpsw/change",
            data: JSON.stringify (this.state.values),
            success: this.changePasswordSuccess,
            error: this.changePasswordError,
            contentType: "application/json",
            dataType: 'json'
            });
        }

        changePasswordSuccess(data){
            this.props.onloading(false);
            this.showAlert('Mot de passe changé');
            history.replace("/login");
        }

        changePasswordError(data){
            this.props.onloading(false);
            var errorCode = data.responseJSON.code;
            this.showAlert(Errors.getErrorMessage(errorCode), 'danger');
        }

        showAlert(message, color='success'){
                this.props.onError(message, color);
        }

        render(){
            if (this.state.valid) {
                return (
                        <div className='changepsw'>
                                <Card body className='changepsw-card'>
                                        <CardTitle>{Text.text.changepassword_label}</CardTitle>
                                        <Form className='form' onKeyPress={this.onKeyPress}>
                                                <FormGroup className='password'>
                                                        <Label for="password">{Text.text.password}</Label>
                                                        <Input onBlur={this.onBlur} onChange={this.onChange} type='password' name="password" id="password" autoComplete="current-password" value={this.state.values.password} />
                                                </FormGroup>
                                                <Button color="success" onClick={this.onChangePassword}>{Text.text.changepassword_bt}</Button>{' '}
                                        </Form>
                                </Card>
                        </div>)
            }
            else {
              return (
                      <div className='changepsw'>
                      </div>)
            }
        }
}

module.exports = ChangeUserPassword;
