import React from 'react'
import jquery from 'jquery'
import { Card, CardBody, CardTitle, Button} from 'reactstrap';


class RegisterPanel extends React.Component{

        constructor(props) {
                super(props);
                this.onRegister = this.onRegister.bind(this);
        }

        onRegister(){
            this.props.onRegister();
        }

        render(){
                var disabled = false;
                if (this.props.disabled)
                        disabled = this.props.disabled;
                return (
                        <div className='registerpanel'>
                                <Card>
                                        <CardBody>
                                          <CardTitle>Vous y aller?</CardTitle>
                                          <Button color="success" onClick={this.onRegister} disabled={disabled}>Oui</Button>
                                        </CardBody>
                                </Card>
                        </div>
                );
        }
}

module.exports = RegisterPanel;
