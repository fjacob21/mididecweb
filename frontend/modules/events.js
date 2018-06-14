import React from 'react'
import jquery from 'jquery'
import EventSmall from './eventsmall'
import EventBig from './eventbig'
import Event from './event'
import User from './user'
import createHistory from "history/createHashHistory"
import Errors from './errors'
import Text from './localization/text'

const history = createHistory();

class Events extends React.Component{
        constructor(props) {
                super(props);
                this.state = {
                        event: null,
                        invalid: true,
                        disableRegister: false
                        };
                jquery.ajax({
                type: 'GET',
                url: "/mididec/api/v1.0/events/"+ this.props.match.params.id,
                success: this.success.bind(this),
                error: this.error.bind(this),
                contentType: "application/json",
                dataType: 'json'
                });

                this.onRegister = this.onRegister.bind(this);
                this.registerSuccess = this.registerSuccess.bind(this);
                this.registerError = this.registerError.bind(this);
                this.onCancel = this.onCancel.bind(this);
                this.cancelSuccess = this.cancelSuccess.bind(this);
                this.cancelError = this.cancelError.bind(this);
        }

        success(data){
                this.state.event = new Event(data.event);
                this.state.invalid = false;
                this.setState(this.state);
        }

        error(data){
                var errorCode = data.responseJSON.code;
                this.showAlert(Errors.getErrorMessage(errorCode), 'danger');
        }

        showAlert(message, color='success'){
                this.props.onError(message, color);
        }

        onRegister(userinfo){
            var user = User.getSession();
            if (!user) {
                history.replace("/login");
            }
            else {
                this.props.onloading(true);
                this.state.disableRegister = true;
                this.setState(this.state);
                var data = {'loginkey': user.loginkey};
                jquery.ajax({
                type: 'POST',
                url: "/mididec/api/v1.0/events/"+ this.props.match.params.id + "/register",
                data: JSON.stringify (data),
                success: this.registerSuccess,
                error: this.registerError,
                contentType: "application/json",
                dataType: 'json'
                });
            }
        }

        registerSuccess(data){
            this.props.onloading(false);
            switch(data.result){
            case 1:
                    this.showAlert(Text.text.event_register_success_msg)
            break;
            case 2:
                    this.showAlert(Text.text.event_register_already_registered_msg, 'danger')
            break;
            case 3:
                    this.showAlert(Text.text.event_register_waiting_msg, 'warning')
            break;
            case 4:
                    this.showAlert(Text.text.event_register_already_waiting_msg, 'danger')
            break;
            };
            this.state.event = new Event(data.event);
            this.state.disableRegister = false;
            this.setState(this.state);
        }

        registerError(data){
            this.props.onloading(false);
            var errorCode = data.responseJSON.code;
            this.showAlert(Errors.getErrorMessage(errorCode), 'danger');
            this.state.disableRegister = false;
            this.setState(this.state);
        }

        onCancel(){
            this.props.onloading(true);
            var user = User.getSession();
            var data = {'loginkey': user.loginkey};
            this.state.disableRegister = true;
            this.setState(this.state);
            jquery.ajax({
            type: 'POST',
            url: "/mididec/api/v1.0/events/"+ this.props.match.params.id + "/unregister",
            data: JSON.stringify (data),
            success: this.cancelSuccess,
            error: this.cancelError,
            contentType: "application/json",
            dataType: 'json'
            });
        }

        cancelSuccess(data){
            this.props.onloading(false);
            this.showAlert(Text.text.event_unregister_success_msg);
            this.state.event = new Event(data.event);
            this.state.disableRegister = false;
            this.setState(this.state);
        }

        cancelError(data){
            this.props.onloading(false);
            var errorCode = data.responseJSON.code;
            this.showAlert(Errors.getErrorMessage(errorCode), 'danger');
            this.state.disableRegister = false;
            this.setState(this.state);
        }

        render(){
                if (this.state.event != null) {
                        return (
                                <div className='events'>
                                        <EventSmall event={this.state.event} onRegister={this.onRegister} onCancel={this.onCancel} disableRegister={this.state.disableRegister}/>
                                        <EventBig event={this.state.event} onRegister={this.onRegister} onCancel={this.onCancel} disableRegister={this.state.disableRegister}/>
                                </div>
                        );
                }
                else {
                        return (
                                <div className='events'>
                                </div>)
                }
        }
}

module.exports = Events;
