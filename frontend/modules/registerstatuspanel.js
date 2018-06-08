import React from 'react'
import jquery from 'jquery'
import { Card, CardBody, CardTitle, Button } from 'reactstrap';
import Text from './localization/text'

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
                        status = Text.text.register_status_registered;
                else if (this.props.status == 'waiting')
                        status =Text.text.register_status_waitinglist;
                var disabled = false;
                if (this.props.disabled)
                        disabled = this.props.disabled;
                return (
                        <div className='registerpanel'>
                                <Card>
                                        <CardBody>
                                          <CardTitle>{status}</CardTitle>
                                          <Button color="danger" onClick={this.onCancel} disabled={disabled}>{Text.text.unregister}</Button>
                                        </CardBody>
                                </Card>
                        </div>
                );
        }
}

module.exports = RegisterStatusPanel;
