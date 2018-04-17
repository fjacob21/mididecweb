import React from 'react'
import jquery from 'jquery'
import EventSmall from './eventsmall'
import EventBig from './eventbig'

class Events extends React.Component{
        constructor(props) {
                super(props);
                console.debug('Start');
                this.state = {event: null, invalid: true};
                jquery.ajax({
                type: 'GET',
                url: "/mididec/api/v1.0/events/"+ this.props.match.params.id,
                success: this.success.bind(this),
                error: this.error,
                contentType: "application/json",
                dataType: 'json'
                });

                this.onRegister = this.onRegister.bind(this);
                this.registerSuccess = this.registerSuccess.bind(this);
                this.registerError = this.registerError.bind(this);
        }

        success(data){
                this.state.event = data.event;
                this.state.invalid = false;
                this.setState(this.state);
        }

        error(){

        }

        onRegister(userinfo){
                var data = {
                        name: userinfo.name,
                        email: userinfo.email,
                        phone: userinfo.phone,
                        sendremindemail: userinfo.useEmail,
                        sendremindsms: userinfo.useSms
                };
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

        registerSuccess(data){
                switch(data.result){
                case 1:
                        console.debug('Registered');
                break;
                case 2:
                        console.debug('Already Registered');
                break;
                case 3:
                        console.debug('Added on the waiting list');
                break;
                case 4:
                        console.debug('Already Added on the waiting list');
                break;
                };

        }

        registerError(data){
                console.error('Not Registered', data);
        }

        render(){
                if (this.state.event != null) {
                        return (
                                <div className='events'>
                                        <EventSmall event={this.state.event} onRegister={this.onRegister}/>
                                        <EventBig event={this.state.event} onRegister={this.onRegister}/>
                                </div>
                        );
                }
                else {
                        return (
                                <div className='event'>
                                </div>)

                }
        }
}

module.exports = Events;
