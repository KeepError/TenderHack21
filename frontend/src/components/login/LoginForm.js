import { Button, Modal, Form, FloatingLabel } from 'react-bootstrap';
import React from 'react';
import InnField from './InnField';

function LoginForm(props) {
    return <Form>  
            <InnField onChange={props.handleFormValueChanged}/>

            <Form.Group controlId="formBasicEmail">
                <Button 
                    variant="primary" 
                    className="float-right bg-red-600" 
                    onClick={props.handleSubmit}>
                        Отправить
                </Button>
            </Form.Group>
    </Form>
}
 
export default LoginForm;