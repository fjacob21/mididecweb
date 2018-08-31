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

class ResetUserPassword extends React.Component{
        constructor(props) {
                super(props);
                this.state = {
                      values: { username: '',
                          email: ''}
                };
                this.onResetPsw = this.onResetPsw.bind(this);
                this.resetPswSuccess = this.resetPswSuccess.bind(this);
                this.resetPswError = this.resetPswError.bind(this);
                this.onChange = this.onChange.bind(this);
                this.onBlur = this.onBlur.bind(this);
                this.onKeyPress = this.onKeyPress.bind(this);
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
                        this.onLogin();
        }

        onResetPsw() {
            this.props.onloading(true);
            jquery.ajax({
            type: 'POST',
            url: "/mididec/api/v1.0/users/resetpsw",
            data: JSON.stringify (this.state.values),
            success: this.resetPswSuccess,
            error: this.resetPswError,
            contentType: "application/json",
            dataType: 'json'
            });
        }

        resetPswSuccess(data){
            this.props.onloading(false);
            this.showAlert('send', 'success');
            history.replace("/login");
        }

        resetPswError(data){
            this.props.onloading(false);
            var errorCode = data.responseJSON.code;
            this.showAlert(Errors.getErrorMessage(errorCode), 'danger');
        }

        showAlert(message, color='success'){
                this.props.onError(message, color);
        }

        render(){
              return (
                      <div className='resetpsw'>
                              <Card body className='reset-card'>
                                      <CardTitle>{Text.text.resetpassword}</CardTitle>
                                      <Form className='form' onKeyPress={this.onKeyPress}>
                                              <FormGroup className='username'>
                                                      <Label for="username">{Text.text.user}</Label>
                                                      <Input onBlur={this.onBlur} onChange={this.onChange} type='text' name="username" id="username" autoComplete="username" value={this.state.values.username} />
                                              </FormGroup>
                                              <FormGroup className='email'>
                                                      <Label for="email">{Text.text.user_email_label}</Label>
                                                      <Input onBlur={this.onBlur} onChange={this.onChange} type='text' name="email" id="email" autoComplete="email" value={this.state.values.email} />
                                              </FormGroup>
                                              <Button color="success" onClick={this.onResetPsw}>{Text.text.resetpassword}</Button>{' '}
                                      </Form>
                              </Card>
                      </div>)
        }
}

module.exports = ResetUserPassword;
