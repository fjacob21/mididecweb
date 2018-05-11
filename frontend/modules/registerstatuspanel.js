import React from 'react'
import jquery from 'jquery'
import { Card, CardBody, CardTitle, Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';


class RegisterStatusPanel extends React.Component{

        constructor(props) {
                super(props);
                this.onCancel = this.onCancel.bind(this);
        }

        onCancel(){
            this.props.onCancel();
        }

        render(){
                var status = '';
                if (this.props.status == 'attending')
                        status = 'Vous êtes inscrit';
                else if (this.props.status == 'waiting')
                        status = 'Vous êtes sur la liste d\'attente';
                return (
                        <div className='registerpanel'>
                                <Card>
                                        <CardBody>
                                          <CardTitle>{status}</CardTitle>
                                          <Button color="danger" onClick={this.onCancel}>Cancelation</Button>
                                        </CardBody>
                                </Card>
                        </div>
                );
        }
}

module.exports = RegisterStatusPanel;
