import React, { Component } from 'react';
import Header from './Header';
import { Container, Row } from 'react-bootstrap';
import UserInfo from './UserInfo';
import Contents from './Contents'

class Portal extends Component {
    render() { 
        return <Container fluid className="p-0">
            <Header/>
            <UserInfo/>
            <Contents/>
        </Container>;
    }
}
 
export default Portal;