import React from 'react'
import jquery from 'jquery'
import UserInfo from './userinfo'
import { Alert, Card, CardBody, CardTitle, Button, Modal, ModalHeader, ModalBody, ModalFooter, Form, FormGroup, Label, Input  } from 'reactstrap';

class MailingList extends React.Component{
        constructor(props) {
                super(props);
                this.state = {
                      registerValid: false,
                      unregisterValid: false,
                      modal: false,
                      userinfo: null,
                      email: '',
                      alert: {
                              visible: false,
                              message: '',
                              color: 'success'
                              }
                };

                this.onRegisterBegin = this.onRegisterBegin.bind(this);
                this.onUnregister = this.onUnregister.bind(this);
                this.onRegister = this.onRegister.bind(this);
                this.onCancel = this.onCancel.bind(this);
                this.onUserInfoChange = this.onUserInfoChange.bind(this);
                this.onChange = this.onChange.bind(this);
                this.registerSuccess = this.registerSuccess.bind(this);
                this.registerError = this.registerError.bind(this);
                this.unregisterSuccess = this.unregisterSuccess.bind(this);
                this.unregisterError = this.unregisterError.bind(this);
                this.onDismiss = this.onDismiss.bind(this);
        }

        showAlert(message, color='success'){
                this.state.alert.color = color;
                this.state.alert.visible = true;
                this.state.alert.message = message;
                this.setState(this.state);
        }

        onDismiss() {
                this.state.alert.visible = false;
                this.setState(this.state);
        }

        onRegisterBegin() {
                this.state.modal = !this.state.modal;
                this.setState(this.state);
        }

        onRegister() {
            jquery.ajax({
            type: 'POST',
            url: "/mididec/api/v1.0/mailinglist/register",
            data: JSON.stringify (this.state.userinfo),
            success: this.registerSuccess,
            error: this.registerError,
            contentType: "application/json",
            dataType: 'json'
            });
        }

        registerSuccess(data){
            this.showAlert('Vous êtes maintenant inscrit sur la liste de diffusion')
            this.state.modal = !this.state.modal;
            this.setState(this.state);
        }

        registerError(data){
            this.showAlert('Une erreur est s\'urvenue lors de l\'inscription', 'danger');
            this.state.modal = !this.state.modal;
            this.setState(this.state);
        }

        unregisterSuccess(data){
            this.showAlert('Vous êtes maintenant désabonné à la liste de diffusion');
            this.state.email = '';
            this.setState(this.state);
        }

        unregisterError(data){
            this.showAlert('Une erreur est s\'urvenue lors de le désabonnement', 'danger');
            this.state.email = '';
        }

        onCancel() {
            this.state.modal = !this.state.modal;
            this.setState(this.state);
        }

        onUnregister() {
            var data = {email: this.state.email};
            jquery.ajax({
            type: 'POST',
            url: "/mididec/api/v1.0/mailinglist/unregister",
            data: JSON.stringify (data),
            success: this.unregisterSuccess,
            error: this.unregisterError,
            contentType: "application/json",
            dataType: 'json'
            });
        }

        onChange(e){
                this.state.email = e.target.value;
                this.state.unregisterValid = false;
                var at = this.state.email.indexOf('@');
                var dot = this.state.email.indexOf('.');
                if (this.state.email != '' && at != -1 && dot != -1 && at < dot && dot+1 < this.state.email.length )
                        this.state.unregisterValid = true;
                this.setState(this.state);
        }

        onUserInfoChange(obj, userinfo){
                this.state.userinfo = obj;
                this.state.registerValid = false;
                var at = obj.email.indexOf('@');
                var dot = obj.email.indexOf('.');
                if (obj.name != '' && obj.email != '' && at != -1 && dot != -1 && at < dot && dot+1 < obj.email.length )
                        this.state.registerValid = true;
                this.setState(this.state);
        }

        render(){
                return (
                        <div className='mailinglist'>
                            <Alert color={this.state.alert.color} isOpen={this.state.alert.visible} toggle={this.onDismiss}>
                                    {this.state.alert.message}
                            </Alert>
                            <Card>
                                <CardBody>
                                    <CardTitle>Inscription à la liste de diffusion</CardTitle>
                                    <Button color="success" onClick={this.onRegisterBegin}>Inscription</Button>
                                </CardBody>
                            </Card>
                            <Card>
                                <CardBody>
                                    <CardTitle>Se désaboner de la liste de diffusion</CardTitle>
                                    <FormGroup className='email'>
                                            <Label for="emsail">Courriel <font size="3" color="red">*</font></Label>
                                            <div><Input onChange={this.onChange} type='email' name="email" id="email" placeholder="test@test.com" value={this.state.email}/></div>
                                    </FormGroup>
                                    <Button color="success" onClick={this.onUnregister} disabled={!this.state.unregisterValid}>Se désaboner</Button>
                                </CardBody>
                            </Card>
                            <Modal isOpen={this.state.modal} toggle={this.onCancel} className={this.props.className}>
                                    <ModalHeader toggle={this.toggle}>Informations</ModalHeader>
                                    <ModalBody>
                                        <UserInfo onInfoChange={this.onUserInfoChange}/>
                                    </ModalBody>
                                    <ModalFooter>
                                            <Button color="primary" onClick={this.onRegister} disabled={!this.state.registerValid}>Sinscrire</Button>
                                            <Button color="secondary" onClick={this.onCancel}>Cancel</Button>
                                    </ModalFooter>
                            </Modal>
                        </div>)
        }
}

module.exports = MailingList;
