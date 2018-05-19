import React , { Component, PropTypes } from 'react'
import { render } from 'react-dom'
import { hashHistory } from 'react-router'
import { HashRouter , Link, Route } from 'react-router-dom'
import { browserHistory} from 'react-router'
import { Button, Form, FormGroup, Label, Input, Alert, Card, CardTitle } from 'reactstrap';
import Navbar from './navbar'
import Home from './home'
import Events from './events'
import CreateEvent from './createevent'
import CreateUser from './createuser'
import UpdateUser from './updateuser'
import UsersAdmin from './usersadmin'
import Login from './login'

class App extends React.Component{
        constructor(props) {
                super(props);
                this.state = {
                      alert: {
                              visible: false,
                              message: '',
                              color: 'success'
                          }
                };
                this.onError = this.onError.bind(this);
                this.hideAlert = this.hideAlert.bind(this);
        }

        onError(message, color){
                this.showAlert(message, color);
        }

        hideAlert(){
                this.state.alert.visible = false;
                this.setState(this.state);
        }

        showAlert(message, color='success'){
                this.state.alert.color = color;
                this.state.alert.visible = true;
                this.state.alert.message = message;
                this.setState(this.state);
                setTimeout(this.hideAlert, 3000);
        }

        componentDidMount(){
        }

        componentWillUnmount(){
        }

        render(){
                return (
                        <div className='app'>
                                <Navbar prev='' next=''></Navbar>
                                <div className='error'>
                                        <Alert className='error' color={this.state.alert.color} isOpen={this.state.alert.visible} toggle={this.onDismiss} transitionAppearTimeout={150} transitionLeaveTimeout={150}>
                                                {this.state.alert.message}
                                        </Alert>
                                </div>
                                <div className='content'>
                                        <Route exact path="/" render={(props) => <Home {...props} onError={this.onError}/>} />
                                        <Route path="/login" render={(props) => <Login {...props} onError={this.onError}/>} />
                                        <Route path="/events/:id" render={(props) => <Events {...props} onError={this.onError}/>} />
                                        <Route path="/createevent" render={(props) => <CreateEvent {...props} onError={this.onError}/>} />
                                        <Route path="/users/:id/update" render={(props) => <UpdateUser {...props} onError={this.onError}/>} />
                                        <Route path="/createuser" render={(props) => <CreateUser {...props} onError={this.onError}/>} />
                                        <Route path="/usersadmin" render={(props) => <UsersAdmin {...props} onError={this.onError}/>} />
                                </div>

                        </div>)
        }
}

module.exports = App;
