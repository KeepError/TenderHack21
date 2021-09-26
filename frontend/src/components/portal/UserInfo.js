import { Container, Row } from "react-bootstrap";

function UserInfo() {
    return <Row className="m-0 border shadow bg-white">
        <Container>
            <Row>
                <h1 className="p-3 font-bold text-5xl font-sans text-center">Рекомендательная платформа</h1>
            </Row>
        </Container>
    </Row>;
}

export default UserInfo;