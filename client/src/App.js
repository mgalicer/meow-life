import React, { Component } from 'react';
import './App.css';

class App extends Component {

  render() {
    return (
      <div className="App">
        <h2>Meow Life</h2>
        <UploadPhoto/>
      </div>
    );
  }
}

class UploadPhoto extends Component {
  constructor(props) {
    super(props)
    this.handleSubmit = this.handleSubmit.bind(this);
    this.fileInput = React.createRef();
    let photo = require('./meow.jpg');
    this.state = {
      photo: photo
    }
  }

  handleSubmit(event) {
    event.preventDefault();
    let file = this.fileInput.current.files[0]
    let fileReader = new FileReader()

    fileReader.onload = (e) => {
      localStorage.setItem(file.name, fileReader.result)
      let localFile = localStorage.getItem(file.name)
      this.setState({photo: localFile})
    };

    fileReader.readAsDataURL(file);
  }

  render() {
    return (
      <form onSubmit={(e) => this.handleSubmit(e)}>
        <label>
          <Photo src={this.state.photo}/>
          <input type="file" ref={this.fileInput}/>
        </label>
        <button type="submit">Submit</button>
      </form>
    );
  }
}

class Photo extends Component {
  constructor(imagePath) {
    super()
  }

  render() {
    return (
      <img className="Photo" src={this.props.src} alt="cat"></img>
    );
  }
}

export default App;
