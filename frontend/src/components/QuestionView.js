import React from 'react';
import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';
import View from './View';

class QuestionView extends View {
  constructor(props) {
    super(props);
    this.state = {
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: {},
      currentCategory: null,
    };
  }

  componentDidMount() {
    super.componentDidMount()
    this.getQuestions();
  }

  getQuestions() {
    $.ajax({
      url: this.url(`questions?page=${this.state.page}`), //TODO: update request URL
      type: 'GET',
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category,
        });
        return;
      },
      error: (error) => {
        this.handleError(error)
      },
    });
  }

  selectPage(num) {
    this.setState({ page: num });
    this.getQuestions();
  }

  createPagination() {
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / 10);
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? 'active' : ''}`}
          onClick={() => {
            this.selectPage(i);
          }}
        >
          {i}
        </span>
      );
    }
    return pageNumbers;
  }

  getByCategory = (id) => {
    $.ajax({
      url: this.url(`categories/${id}/questions`), //TODO: update request URL
      type: 'GET',
      success: (result) => {
        if(result.success) {
          this.setState({
            questions: result.questions,
            totalQuestions: result.total_questions,
            currentCategory: result.current_category,
          });
        } else alert("No available question");
        return;
      },
      error: (error) => {
        this.handleError(error);
      },
    });
  };

  submitSearch = (searchTerm) => {
    $.ajax({
      url: this.url("questions"), //TODO: update request URL
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({ searchTerm: searchTerm }),
      crossDomain: true,
      success: (result) => {
        if(result.success) {
          this.setState({
            questions: result.questions,
            totalQuestions: result.total_questions,
            currentCategory: result.current_category,
          });
        } else {
          alert("Not found.");
        }
        return;
      },
      error: (error) => {
        this.handleError(error);
      },
    });
  };

  questionAction = (id) => (action) => {
    if (action === 'DELETE') {
      if (window.confirm('are you sure you want to delete the question?')) {
        $.ajax({
          url: this.url(`questions/${id}`), //TODO: update request URL
          type: 'DELETE',
          success: (result) => {
            this.setState({
              "questions": this.state.questions.filter(
                question => question.id !== id)
            });
          },
          error: (error) => {
            this.handleError(error);
          },
        });
      }
    }
  };

  render() {
    return (
      <div className='question-view'>
        {super.render()}
        <div className='categories-list'>
          <h2
            onClick={() => {
              this.getQuestions();
            }}
          >
            Categories
          </h2>
          <ul>
            {Object.keys(this.state.categories).map((id) => (
              <li
                key={id}
                onClick={() => {
                  this.getByCategory(id);
                }}
              >
                {this.state.categories[id]}
                <img
                  className='category'
                  alt={`${this.state.categories[id].toLowerCase()}`}
                  src={`${this.state.categories[id].toLowerCase()}.svg`}
                />
              </li>
            ))}
          </ul>
          <Search submitSearch={this.submitSearch} />
        </div>
        <div className='questions-list'>
          <h2>Questions</h2>
          {this.state.questions.map((q, ind) => (
            <Question
              key={q.id}
              question={q.question}
              answer={q.answer}
              category={this.state.categories[q.category]}
              difficulty={q.difficulty}
              questionAction={this.questionAction(q.id)}
            />
          ))}
          <div className='pagination-menu'>{this.createPagination()}</div>
        </div>
      </div>
    );
  }
}

export default QuestionView;
