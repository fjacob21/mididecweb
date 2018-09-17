import React , { Component, PropTypes } from 'react'
import { browserHistory} from 'react-router'
import jquery from 'jquery'
import createHistory from "history/createHashHistory"
import User from './user'
import Errors from './errors'
import FormQuery from './formquery'
import { Button, Form, FormGroup, Label, Input, Card, CardTitle } from 'reactstrap';
import Text from './localization/text'
import queryString from 'query-string';

const history = createHistory();

class Login extends React.Component{
        constructor(props) {
                super(props);
                this.state = {
                      values: { userid: '',
                          password: ''}
                };
                this.onLogin = this.onLogin.bind(this);
                this.loginSuccess = this.loginSuccess.bind(this);
                this.loginError = this.loginError.bind(this);
                this.onResetPassword = this.onResetPassword.bind(this);
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

        onLogin() {
            let params = queryString.parse(this.props.location.search);
            if (params.register != undefined)
              this.state.values['register'] = params.register;
            this.props.onloading(true);
            jquery.ajax({
            type: 'POST',
            url: "/mididec/api/v1.0/users/" + this.state.values.userid + '/login',
            data: JSON.stringify (this.state.values),
            success: this.loginSuccess,
            error: this.loginError,
            contentType: "application/json",
            dataType: 'json'
            });
        }

        loginSuccess(data){
            this.props.onloading(false);
            sessionStorage.setItem('userinfo', JSON.stringify(data.user));
            if (data.register == undefined)
              history.replace("/");
            else
              history.replace("/events/"+data.register);
        }

        loginError(data){
            this.props.onloading(false);
            var errorCode = data.responseJSON.code;
            this.showAlert(Errors.getErrorMessage(errorCode), 'danger');
        }

        onResetPassword(data){
            this.props.onloading(false);
            history.replace("/resetpsw");
        }

        showAlert(message, color='success'){
                this.props.onError(message, color);
        }

        render(){
                return (
                        <div className='login'>
                                <Card body className='login-card'>
                                        <CardTitle>{Text.text.login}</CardTitle>
                                        <Form className='form' onKeyPress={this.onKeyPress}>
                                                <FormGroup className='userid'>
                                                        <Label for="userid">{Text.text.user}</Label>
                                                        <Input onBlur={this.onBlur} onChange={this.onChange} type='text' name="userid" id="userid" autoComplete="username" value={this.state.values.userid} />
                                                </FormGroup>
                                                <FormGroup className='password'>
                                                        <Label for="password">{Text.text.password}</Label>
                                                        <Input onBlur={this.onBlur} onChange={this.onChange} type='password' name="password" id="password" autoComplete="current-password" value={this.state.values.password} />
                                                </FormGroup>
                                                <Button color="success" onClick={this.onLogin}>{Text.text.login}</Button>{' '}
                                                <Button color="danger" onClick={this.onResetPassword}>{Text.text.resetpassword}</Button>{' '}
                                        </Form>
                                </Card>
                        </div>)
        }
}

module.exports = Login;
