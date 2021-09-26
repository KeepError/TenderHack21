import React from 'react';
import LoginModal from './login/LoginModal';
import Portal from './portal/Portal';

class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      innInfo: 0
    }
  }

  render() {
    return (
      <div className="bg-gray-300 min-h-screen">
        <LoginModal onInnObjectSubmit={(inn) => this.setState({innInfo : inn})}/>
        <Portal/>
      </div>
    );
  }
}

export default App;
