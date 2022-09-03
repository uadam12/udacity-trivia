import React, { Component } from "react";
import $ from 'jquery';
import '../stylesheets/View.css';

class View extends Component {
  message(message) {
    this.setState({message: message});

    window.setTimeout(() => {
        this.setState({message: ''});
    }, 5000);
  }

  handleError(error) {
    let msg, handled = true;

    try {
        msg = error.responseJSON.message;
    } catch(e) {
        msg = "Something went wrong.";
        handled = false;
    }

    this.message(msg);

    return handled;
  }
  componentDidMount() {
    $.ajax({
      url: this.url('categories'), //TODO: update request URL
      type: 'GET',
      success: (result) => {
        this.setState({categories: result.categories});
      },
      error: error => {
        this.handleError(error);
      },
    });
  }

  url(path) {
    return `http://localhost:5000/api/v1/${path}`;
  }

  render() {
    return <div className='message'>
        {this.state.message}
    </div>
  }
}

export default View;