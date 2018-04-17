import React from 'react'
import jquery from 'jquery'
import DateFormater from './dateformater'
import UserInfo from './userinfo'
import { Card, CardBody, CardTitle, Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';

class EventBig extends React.Component{
        constructor(props) {
                super(props);
                this.state = {
                      valid: false,
                      modal: false,
                      userinfo: null
                };
                this._start = new DateFormater(this.props.event.start);
                this._end = new DateFormater(this.props.event.end);
                this.toggle = this.toggle.bind(this);
                this.onCancel = this.onCancel.bind(this);
                this.onRegister = this.onRegister.bind(this);
                this.onUserInfoChange = this.onUserInfoChange.bind(this);
        }

        toggle() {
                this.state.modal = !this.state.modal;
                this.setState(this.state);
        }

        onCancel() {
                this.state.modal = false;
                this.setState(this.state);
        }

        onRegister(){
                this.state.modal = false;
                this.setState(this.state);
                this.props.onRegister(this.state.userinfo);
        }

        onUserInfoChange(obj, userinfo){
                this.state.userinfo = obj;
                this.state.valid = false;
                var at = obj.email.indexOf('@');
                var dot = obj.email.indexOf('.');
                if (obj.name != '' && obj.email != '' && at != -1 && dot != -1 && at < dot && dot+1 < obj.email.length )
                        this.state.valid = true;
                this.setState(this.state);
        }

        render(){
                var dateText = this._start.getDateText();
                var timeText = this._start.getTimeText() + ' à ';
                timeText += this._end.getTimeText();
                var icalurl = '/mididec/api/v1.0/events/' + this.props.event.uid + '/ical';
                return (
                        <div className='eventbig'>
                                <div className='head'>
                                        <div className='head-info'>
                                                <div className='start'> {dateText} </div>
                                                <div className='title'> {this.props.event.title} </div>
                                                <div className='organizer'> Organiser par {this.props.event.organizer_name} </div>
                                        </div>
                                        <div className='head-register'>
                                                <Card>
                                                        <CardBody>
                                                          <CardTitle>Vous y aller?</CardTitle>
                                                          <Button color="success" onClick={this.toggle}>Oui</Button>
                                                        </CardBody>
                                                </Card>
                                        </div>
                                </div>
                                <div className='body'>
                                        <div className='detail'>
                                                <div className='detaillabel'> Détail </div>
                                                <div className='description'>{this.props.event.description} </div>
                                        </div>
                                        <div className='info'>
                                                <div className='duration'>
                                                        <img className='timeicon' src='res/drawables/time-icon.png'></img>
                                                        <div className='timetext'>
                                                                <div className='date'>{dateText}</div>
                                                                <div className='time'>{timeText}</div>
                                                                <a href={icalurl}>Ajouter au calendrier</a>
                                                        </div>
                                                </div>
                                                <div className='location'>
                                                        <img className='locationicon' src='res/drawables/location-icon.png'></img>
                                                        <div className='locationtext'>
                                                                {this.props.event.location}
                                                        </div>
                                                </div>
                                        </div>
                                </div>
                                <Modal isOpen={this.state.modal} toggle={this.toggle} className={this.props.className}>
                                        <ModalHeader toggle={this.toggle}>Informations</ModalHeader>
                                        <ModalBody>
                                            <UserInfo onInfoChange={this.onUserInfoChange}/>
                                        </ModalBody>
                                        <ModalFooter>
                                                <Button color="primary" onClick={this.onRegister} disabled={!this.state.valid}>S'inscrire</Button>
                                                <Button color="secondary" onClick={this.onCancel}>Cancel</Button>
                                        </ModalFooter>
                                </Modal>
                        </div>);
        }
}

module.exports = EventBig;
