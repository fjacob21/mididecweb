import React from 'react'
import jquery from 'jquery'
import DateFormater from './dateformater'
import { Button, Form, FormGroup, Label, Input } from 'reactstrap';

class UserInfo extends React.Component{
        constructor(props) {
                super(props);
                this.onChange = this.onChange.bind(this);
        }

        onChange(e){
                if (this.props.onInfoChange != undefined) {
                        var obj = {name: this.name.value, email: this.email.value, phone:this.phone.value, useEmail: this.useEmail.checked, useSms: this.useSms.checked}
                        this.props.onInfoChange(obj);
                }
        }

        render(){
                return (
                        <Form className='register'>
                                <FormGroup className='name'>
                                        <Label for="name">Nom <font size="3" color="red">*</font></Label>
                                        <Input onChange={this.onChange} type='text' name="name" id="name" placeholder="Nom" innerRef={(name) => this.name = name}/>
                                </FormGroup>
                                <FormGroup className='email'>
                                        <Label for="emsail">Courriel <font size="3" color="red">*</font></Label>
                                        <div><Input onChange={this.onChange} type='email' name="email" id="email" placeholder="test@test.com" innerRef={(email) => this.email = email}/></div>
                                </FormGroup>
                                <FormGroup className='phone'>
                                        <Label for="phone">Cell.</Label>
                                        <div><Input onChange={this.onChange} type='text' name="phone" id="phone" placeholder="+15551234567" innerRef={(phone) => this.phone = phone}/></div>
                                </FormGroup>
                                <FormGroup check  className='use'>
                                        <Label>
                                                <Input onChange={this.onChange} type='checkbox' innerRef={(useEmail) => this.useEmail = useEmail}/>
                                                Recevoir alerte par courriel
                                        </Label>
                                </FormGroup>
                                <FormGroup check>
                                        <Label>
                                                <Input onChange={this.onChange} type='checkbox' innerRef={(useSms) => this.useSms = useSms}/>
                                                Recevoir alerte par sms
                                        </Label>
                                </FormGroup>
                        </Form>)
        }
}

module.exports = UserInfo;
