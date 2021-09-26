import { Button, Modal, Form, FloatingLabel } from 'react-bootstrap';
import React from 'react';

function InnField(props) {
    return <Form.Group className="mb-3" controlId="formBasicEmail">
            <FloatingLabel controlId="floatingInputGrid" label="ИНН">
                <Form.Control 
                    type="text"
                    defaultValue="291101608569"
                    onChange={props.onChange} />
            </FloatingLabel>
        </Form.Group>;
}

export default InnField;