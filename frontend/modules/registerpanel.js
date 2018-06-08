import React from 'react'
import jquery from 'jquery'
import { Card, CardBody, CardTitle, Button} from 'reactstrap';
import Text from './localization/text'

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
                                          <CardTitle>{Text.text.event_register_question_msg}</CardTitle>
                                          <Button color="success" onClick={this.onRegister} disabled={disabled}>{Text.text.yes}</Button>
                                        </CardBody>
                                </Card>
                        </div>
                );
        }
}

module.exports = RegisterPanel;
