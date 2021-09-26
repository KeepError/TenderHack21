import { Modal } from 'react-bootstrap';
import React, { useState } from 'react';
import LoginForm from './LoginForm';
import axios from 'axios'
import Contents from '../portal/Contents';

class LoginModal extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      showModal: true,
      innValue: "291101608569",
      errorMessage: ""
    };

    axios.interceptors.response.use(
      (resp) => this.handleResponse(resp),
      (error) => this.handleError(error),
    );
  }

  componentDidMount() {
    //this.handleSubmit(); // TODO: Debug code
  }

  handleResponse(resp) {
    if(!resp) return
    //this.props.onInnObjectSubmit(resp.data);
    //console.log(this);
  }

  handleError(err) {
    this.setState({ errorMessage: "Error"});
  }

  handleSubmit() {
    //axios.get("http://192.168.31.127:8080/api/inn/" + this.state.innValue);
    this.setState({ showModal: false});
    this.props.onInnObjectSubmit(this.state.innValue);
  }

  handleFormValueChanged(event) {
    this.setState({
      innValue: event.target.value,
      errorMessage: ""
    });
  }

  render() {
    return (
      <>
        <Modal show={this.state.showModal} centered>
          <Modal.Header>
            <Modal.Title>Авторизация</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <p>{this.state.errorMessage}</p>
            <LoginForm 
              handleSubmit={() => this.handleSubmit()}
              handleFormValueChanged={(event) => this.handleFormValueChanged(event)}/>
          </Modal.Body>
        </Modal>
      </>
    );
  } 
}

export default LoginModal;