import React from 'react'
import jquery from 'jquery'
import { Card, CardBody, CardTitle, Button } from 'reactstrap';


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
                var disabled = false;
                if (this.props.disabled)
                        disabled = this.props.disabled;
                return (
                        <div className='registerpanel'>
                                <Card>
                                        <CardBody>
                                          <CardTitle>{status}</CardTitle>
                                          <Button color="danger" onClick={this.onCancel} disabled={disabled}>Cancelation</Button>
                                        </CardBody>
                                </Card>
                        </div>
                );
        }
}

module.exports = RegisterStatusPanel;
