import React, { Component } from 'react';
import './App.css';

class App extends Component {
//<Photo src={require('./baby.png')}/>
//<Photo src={require('./baby.png')}/>
  render() {
    return (
      <div className="App">
        <h2>Meow Life</h2>
        <div className="photos"> 
          <Photo src={require('./meow.jpg')}/>
          <Photo src={require('./meow.jpg')}/>
        </div>
      </div>
    );
  }
}

class Photo extends Component {
  constructor(imagePath) {
    super()
  }

  render() {
    console.log(this.props)
    return (
      <img className="Photo" src={this.props.src} alt="cat"></img>
    );
  }
}

export default App;
