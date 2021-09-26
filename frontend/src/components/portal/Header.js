import { Col, Container, Image, Row } from "react-bootstrap";
import { Icon } from '@iconify/react';

var logoUrl = "https://zakupki.mos.ru/static/media/pp_logo.80b7ad86.svg"

function Header() {
    return <Row className="w-full shadow p-3 m-0 bg-white">
        <Col md="auto">
            <Image src={logoUrl}/>
        </Col>
        <Col className="space-x-2">
            <Icon className="inline-block h-full" icon="clarity:menu-line" width="36"/>
            <div className="inline-block">Меню</div>
        </Col>
    </Row>
}

export default Header;