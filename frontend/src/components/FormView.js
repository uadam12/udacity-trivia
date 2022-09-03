import React from 'react';
import $ from 'jquery';
import '../stylesheets/FormView.css';
import View from './View';

class FormView extends View {
  constructor() {
    super();
    this.state = {
      question: '',
      answer: '',
      difficulty: 1,
      category: 1,
      categories: {},
    };
  }


  submitQuestion = (event) => {
    event.preventDefault();
    $.ajax({
      url: this.url('questions'), //TODO: update request URL
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        question: this.state.question,
        answer: this.state.answer,
        difficulty: this.state.difficulty,
        category: this.state.category,
      }),
      crossDomain: true,
      success: (result) => {
        document.getElementById('add-question-form').reset();
        return;
      },
      error: (error) => {
        this.handleError(error);
      },
    });
  };

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  };

  render() {
    return (
      <div id='add-form'>
        {super.render()}
        <h2>Add a New Trivia Question</h2>
        <form
          className='form-view'
          id='add-question-form'
          onSubmit={this.submitQuestion}
        >
          <label>
            Question
            <input type='text' name='question' onChange={this.handleChange} />
          </label>
          <label>
            Answer
            <input type='text' name='answer' onChange={this.handleChange} />
          </label>
          <label>
            Difficulty
            <select name='difficulty' onChange={this.handleChange}>
              <option value='1'>1</option>
              <option value='2'>2</option>
              <option value='3'>3</option>
              <option value='4'>4</option>
              <option value='5'>5</option>
            </select>
          </label>
          <label>
            Category
            <select name='category' onChange={this.handleChange}>
              {Object.keys(this.state.categories).map((id) => {
                return (
                  <option key={id} value={id}>
                    {this.state.categories[id]}
                  </option>
                );
              })}
            </select>
          </label>
          <input type='submit' className='button' value='Submit' />
        </form>
      </div>
    );
  }
}

export default FormView;
