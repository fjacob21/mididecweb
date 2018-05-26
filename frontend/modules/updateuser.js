import React , { Component, PropTypes } from 'react'
import { browserHistory} from 'react-router'
import jquery from 'jquery'
import createHistory from "history/createHashHistory"
import User from './user'
import Errors from './errors'
import FormQuery from './formquery'
import { Button, Form, FormGroup, Label, Input, Card, CardTitle, FormFeedback } from 'reactstrap';

const history = createHistory();

class UpdateUser extends React.Component{
        constructor(props) {
                super(props);
                this.state = {
                      valid: false,
                      validation: {
                              emailok: true,
                              aliasok: true
                      },
                      values: { name: '',
                                email: '',
                                password: '',
                                alias: '',
                                phone: '',
                                useemail: true,
                                usesms: false,
                                profile: '',
                                access: 0,
                        }
                };
                this.getUser();
                this.onCancel = this.onCancel.bind(this);
                this.onUpdate = this.onUpdate.bind(this);
                this.updateSuccess = this.updateSuccess.bind(this);
                this.updateError = this.updateError.bind(this);
                this.validateSuccess = this.validateSuccess.bind(this);
                this.validateError = this.validateError.bind(this);
                this.onChange = this.onChange.bind(this);
                this.onCheck = this.onCheck.bind(this);
                this.onKeyPress = this.onKeyPress.bind(this);
                this.handleFileUpload = this.handleFileUpload.bind(this);
                this.onFile = this.onFile.bind(this);
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
                        (dot+1) < this.state.values.email.length )
                            this.state.valid = true;
                }
                this.setState(this.state);
        }

        validateError(data){
            var errorCode = data.responseJSON.code;
            this.showAlert(Errors.getErrorMessage(errorCode), 'danger');
        }

        onUpdate() {
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
            this.showAlert('Update success', 'success');
            this.getUser();
        }

        updateError(data){
            var errorCode = data.responseJSON.code;
            this.showAlert(Errors.getErrorMessage(errorCode), 'danger');
        }

        showAlert(message, color='success'){
                this.props.onError(message, color);
        }

        handleFileUpload(event){
                var user = User.getSession();
                const file = event.target.files[0];
                const formData = new FormData()
                formData.append('avatar', file, file.name);
                jquery.ajax({
                type: 'POST',
                url: "/mididec/api/v1.0/users/" + this.props.match.params.id+"/avatar?loginkey="+user.loginkey,
                data: formData,
                processData: false,
                contentType: false,
                success: this.updateSuccess,
                error: this.updateError
                });
        }

        onFile(){
                document.getElementById('profile_pic').click();
        }
        render(){
                var user = User.getSession();
                var access = "";
                if (user.isSuperUser)
                        access = (<FormGroup className='profile'>
                                <Label for="access">Access</Label>
                                <div>
                                        <Input type="select" name="access" id="access" onChange={this.onChange} value={this.state.values.access.toString()}>
                                            <option value='0'>Normal</option>
                                            <option value='3'>Manager</option>
                                            <option value='255'>Super</option>
                                        </Input>
                                </div>
                        </FormGroup>);
                var emailErrorMessage = "";
                if (!this.state.validation.emailok)
                        emailErrorMessage = <FormFeedback>Désolé ce courriel est déja utilisé</FormFeedback>
                var aliasErrorMessage = "";
                if (!this.state.validation.aliasok)
                        aliasErrorMessage = <FormFeedback>Désolé cet alias est déja utilisé</FormFeedback>
                var avatar = <i className="material-icons md-light attendee-avatar-default">account_circle</i>
                if (this.state.values.have_avatar) {
                        var avatar_path = "/mididec/api/v1.0/users/" + this.props.match.params.id+"/avatar?" + new Date().getTime();
                        avatar = <img src={avatar_path} className="attendee-avatar"/>
                }
                console.debug('render');
                return (
                        <div className='updateuser'>
                                <Card body className='updateuser-card'>
                                        <CardTitle>Profile</CardTitle>

                                        <Form className='updateuser-form' onKeyPress={this.onKeyPress}>
                                                {avatar}
                                                <FormGroup className='name'>
                                                        <Button onClick={this.onFile}>Changer l'avatar</Button>
                                                        <Input className="file" type="file" id="profile_pic" name="profile_pic" onChange={this.handleFileUpload} accept="image/*"/>
                                                </FormGroup>
                                                <FormGroup className='name'>
                                                        <Label for="name">Nom <font size="3" color="red">*</font></Label>
                                                        <Input onChange={this.onChange} autocomplete='name' type='text' name="name" id="name" placeholder="Nom" value={this.state.values.name} />
                                                </FormGroup>
                                                <FormGroup className='email'>
                                                        <Label for="email">Courriel <font size="3" color="red">*</font></Label>
                                                        <div>
                                                                <Input invalid={!this.state.validation.emailok} autocomplete='email' onChange={this.onChange} type='email' name="email" id="email" placeholder="test@test.com" value={this.state.values.email} />
                                                                {emailErrorMessage}
                                                        </div>
                                                </FormGroup>
                                                <FormGroup className='alias'>
                                                        <Label for="alias">Alias <font size="3" color="red">*</font></Label>
                                                        <div>
                                                                <Input invalid={!this.state.validation.aliasok} autocomplete='alias' onChange={this.onChange} type='text' name="alias" id="alias" placeholder="alias" value={this.state.values.alias} />
                                                                {aliasErrorMessage}
                                                        </div>
                                                </FormGroup>
                                                <FormGroup className='password'>
                                                        <Label for="password">Mot de passe</Label>
                                                        <Input onChange={this.onChange} autocomplete='current-password' type='password' name="password" id="password" value={this.state.values.password} />
                                                </FormGroup>
                                                <FormGroup className='phone'>
                                                        <Label for="phone">Cell.</Label>
                                                        <div><Input onChange={this.onChange} autocomplete='tel' type='text' name="phone" id="phone" placeholder="+15551234567" value={this.state.values.phone} /></div>
                                                </FormGroup>
                                                <FormGroup className='profile'>
                                                        <Label for="profile">Profile</Label>
                                                        <div>
                                                                <Input autocomplete='profile' onChange={this.onChange} type='text' name="profile" id="profile" placeholder="profile" value={this.state.values.profile} />
                                                        </div>
                                                </FormGroup>
                                                {access}
                                                <FormGroup check>
                                                        <Label>
                                                                <Input onChange={this.onCheck} type='checkbox' id="useemail" checked={this.state.values.useemail} />{' '}
                                                                Recevoir alerte par courriel
                                                        </Label>
                                                </FormGroup>
                                                <FormGroup check>
                                                        <Label>
                                                                <Input onChange={this.onCheck} type='checkbox' id="usesms" checked={this.state.values.usesms} />
                                                                Recevoir alerte par sms
                                                        </Label>
                                                </FormGroup>
                                                <Button className='bt-update' color="primary" onClick={this.onUpdate} disabled={!this.state.valid}>Sauvegarder</Button>
                                                <Button color="secondary" onClick={this.onCancel} >Cancel</Button>
                                        </Form>
                                </Card>
                        </div>)
        }
}

module.exports = UpdateUser;
