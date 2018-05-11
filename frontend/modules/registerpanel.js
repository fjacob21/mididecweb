import React from 'react'
import jquery from 'jquery'
import { Card, CardBody, CardTitle, Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';


class RegisterPanel extends React.Component{

        constructor(props) {
                super(props);
        }

        render(){
                return (
                        <div className='registerpanel'>
                                <Card>
                                        <CardBody>
                                          <CardTitle>Vous y aller?</CardTitle>
                                          <Button color="success">Oui</Button>
                                        </CardBody>
                                </Card>
                        </div>
                );
        }
}

module.exports = RegisterPanel;
