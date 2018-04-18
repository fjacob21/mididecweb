import React from 'react'
import jquery from 'jquery'
import EventSmall from './eventsmall'
import EventBig from './eventbig'
import { Alert } from 'reactstrap';

class Events extends React.Component{
        constructor(props) {
                super(props);
                console.debug('Start');
                this.state = {
                        event: null,
                        invalid: true,
                        alert: {
                                visible: false,
                                message: '',
                                color: 'success'
                                }
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
                this.onDismiss = this.onDismiss.bind(this);
        }

        success(data){
                this.state.event = data.event;
                this.state.invalid = false;
                this.setState(this.state);
        }

        error(data){
                this.showAlert('Cette événement n\'est pas disponible!', 'danger');
        }

        onDismiss() {
                this.state.alert.visible = false;
                this.setState(this.state);
        }

        showAlert(message, color='success'){
                this.state.alert.color = color;
                this.state.alert.visible = true;
                this.state.alert.message = message;
                this.setState(this.state);
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
                        this.showAlert('Vous êtes maintenant inscrit a cette évènement')
                break;
                case 2:
                        this.showAlert('Vous êtes déja inscrit a cette évènement', 'danger')
                break;
                case 3:
                        this.showAlert('Malheureusement il ne reste plus de place disponible! Vous etes par contre sur la liste d\'attente.', 'warning')
                break;
                case 4:
                        this.showAlert('Vous êtes déja sur la liste d\'attente', 'danger')
                break;
                };

        }

        registerError(data){
                this.showAlert('Une erreur est survenue lors de l\'enregistrement!!!!', 'danger')
        }

        render(){
                if (this.state.event != null) {
                        return (
                                <div className='events'>
                                        <Alert color={this.state.alert.color} isOpen={this.state.alert.visible} toggle={this.onDismiss}>
                                                {this.state.alert.message}
                                        </Alert>
                                        <EventSmall event={this.state.event} onRegister={this.onRegister}/>
                                        <EventBig event={this.state.event} onRegister={this.onRegister}/>
                                </div>
                        );
                }
                else {
                        return (
                                <div className='events'>
                                        <Alert color={this.state.alert.color} isOpen={this.state.alert.visible} toggle={this.onDismiss}>
                                                {this.state.alert.message}
                                        </Alert>
                                </div>)

                }
        }
}

module.exports = Events;
