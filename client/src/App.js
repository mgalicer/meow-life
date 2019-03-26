import React, { Component } from 'react';
import './App.css';

class App extends Component {
  constructor() {
    super()
    const defaultPhoto = require('./meow.jpg');
    this.classifyPhoto = this.classifyPhoto.bind(this);
    this.state = {
      personPhoto: defaultPhoto,
      catPhoto: defaultPhoto
    }
  }

  classifyPhoto(file) {
    const formData = new FormData();
    formData.append('file', file);

    fetch('http://127.0.0.1:5000/classify', {
      method: 'POST',
      body: formData,
      mode: 'no-cors'
    })
    .then(response => {
      console.log(response)
      this.setState({ catPhoto: response.body })
    }) 
  }

  render() {
    return (
      <div className="App">
        <h2>Meow Life</h2>
        <UploadPhoto classifyPhoto={this.classifyPhoto}/>
        <Photo src={this.state.catPhoto} />
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
      localStorage.setItem(file.name, fileReader.result);
      let localFile = localStorage.getItem(file.name);
      this.setState({photo: localFile});
      this.props.classifyPhoto(localFile);
    };

    fileReader.readAsDataURL(file);
  }

  render() {
    return (
      <form>
        <label>
          <Photo src={this.state.photo}/>
          <input type="file" ref={this.fileInput} onChange={(e) => this.handleSubmit(e)}/>
        </label>
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
