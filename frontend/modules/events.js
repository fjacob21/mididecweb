import React from 'react'
import jquery from 'jquery'
import EventSmall from './eventsmall'
import EventBig from './eventbig'
import Event from './event'
import User from './user'
import createHistory from "history/createHashHistory"
import Errors from './errors'

const history = createHistory();

class Events extends React.Component{
        constructor(props) {
                super(props);
                this.state = {
                        event: null,
                        invalid: true
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
                this.onDismiss = this.onDismiss.bind(this);
        }

        success(data){
                this.state.event = new Event(data.event);
                this.state.invalid = false;
                this.setState(this.state);
        }

        error(data){
                console.debug(data.responseJSON);
                var errorCode = data.responseJSON.code;
                this.showAlert(Errors.getErrorMessage(errorCode), 'danger');
        }

        onDismiss() {
                this.state.alert.visible = false;
                this.setState(this.state);
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
                switch(data.result){
                case 1:
                        this.showAlert('Vous êtes maintenant inscrit a cette événement')
                break;
                case 2:
                        this.showAlert('Vous êtes déja inscrit a cette événement', 'danger')
                break;
                case 3:
                        this.showAlert('Malheureusement il ne reste plus de place disponible! Vous etes par contre sur la liste d\'attente.', 'warning')
                break;
                case 4:
                        this.showAlert('Vous êtes déja sur la liste d\'attente', 'danger')
                break;
                };
                this.state.event = new Event(data.event);
                this.setState(this.state);
        }

        registerError(data){
                this.showAlert('Une erreur est survenue lors de l\'enregistrement!!!!', 'danger')
        }

        onCancel(){
            var user = User.getSession();
            var data = {'loginkey': user.loginkey};
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
                this.showAlert('Vous n\'êtes plus inscrit a cette évènement');
                this.state.event = new Event(data.event);
                this.setState(this.state);
        }

        cancelError(data){
                this.showAlert('Une erreur est survenue lors de la cancellation!!!!', 'danger');
                this.setState(this.state);
        }

        render(){
                if (this.state.event != null) {
                        return (
                                <div className='events'>
                                        <EventSmall event={this.state.event} onRegister={this.onRegister} onCancel={this.onCancel}/>
                                        <EventBig event={this.state.event} onRegister={this.onRegister} onCancel={this.onCancel}/>
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
