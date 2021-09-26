import { Container, Row } from "react-bootstrap";
import React from 'react';
import LoginModal from "../login/LoginModal";

class MyComponent extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        error: null,
        isLoaded: false,
        loadModule: false,
        items: [],
        inn: 0
      };
    }
  
    componentDidMount() {
      fetch("http://192.168.31.127:8080/api/predictions/periodicity/291101608569")
        .then(response => response.json())
        .then(
          (records) => {
            this.setState({
              isLoaded: true,
              items: records.records
            });
            console.log(records);
          },
          // Примечание: важно обрабатывать ошибки именно здесь, а не в блоке catch(),
          // чтобы не перехватывать исключения из ошибок в самих компонентах.
          (error) => {
            this.setState({
              isLoaded: true,
              error
            });
          }
        );
    }
  
    render() {
      const { error, isLoaded, items } = this.state;
      if (error) {
        return <div>Ошибка: {error.message}</div>;
      } else if (!isLoaded) {
        return <div>Загрузка...</div>;
      } else {
        return (
          <ul>
            {items.map(record => (
              <li key={record[0].category_name}>
                {record[0].category_name}
              </li>
            ))
            }
          </ul>
        );
      }
    }
  }


  function Contents(props) {
    return <Row className="m-4 border shadow bg-white">
        <Container>
            <Row>
                <h1 className="p-3 font-bold text-2xl font-sans text-left">Вам могут быть интересны эти закупки</h1>
                <p className="p-3 font-bold">На основе ваших предыдщих закупок:</p>
                <MyComponent></MyComponent>
                <p className="p-3">Подробнее</p>
            </Row>
        </Container>
    </Row>;
}

export default Contents;