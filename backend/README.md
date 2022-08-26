# Backend - Trivia API

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application can:

* Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
* Delete questions.
* Add questions and require that they include question and answer text.
* Search for questions based on a text query string.
* Play the quiz game, randomizing either all questions or within a specific category.

## Table of Content

* [Setting up](#setting-up)
  * [Install Dependencies](#install-dependencies)
  * [Key Pip Dependencies](#key-pip-dependencies)
  * [Set up the Database](#Set-up-the-Database)
  * [Run the Server](#run-the-server)
* [Note](#note)
* [Testing](#testing)
* [Endpoints](#endpoints)
* [Error Handling](#error-handling)

## Setting up

### Install Dependencies

1. **Python 3.x** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

    ```bash
    pip install -r requirements.txt
    ```

### Key Pip Dependencies

* [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

* [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

* [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_DEBUG=True
flask run
```

The `FLASK_DEBUG` variable will detect file changes and restart the server automatically.

[Goto Top](#backend---trivia-api)

## NOTE

One thing to note: for each endpoint, we have define the endpoint and response data. The frontend will be a plentiful resource because it has the endpoints and response data as it expects. We have use:

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It returns any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

[Goto Top](#backend---trivia-api)

## Testing

We wrote at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

[Goto Top](#backend---trivia-api)

### Endpoints

`GET '/api/v1.0/categories'`

* Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
* Request Arguments: None
* Returns: An object with two keys, `success` with `True` as it value and `categories`, that contains an object of `category_id: category_type` key: value pairs.

Sample:

```bash
curl /api/v1.0/categories
```

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

`GET '/api/v1.0/questions'`

* Fetches a list of paginated questions from all categories.
* Request Arguments: None
* Returns: A list of questions in group of 10 questions per page, number of total questions, category, success value.

Sample:

```bash
curl /api/v1/questions
```

```json
{
  "current_category": "all",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": "5",
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": "5",
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"    
    },
    {
      "answer": "Maya Angelou",
      "category": "4",
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": "5",
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": "4",
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": "6",
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every 
soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": "6",
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": "4",
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": "3",
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"    
    },
    {
      "answer": "The Palace of Versailles",
      "category": "3",
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 44
}
```

`POST 'api/v1/questions'`

* Fetches questions based on `searchTerm` if provided.
* Request Argument: `searchTerm`
* Returns list of available questions, total number of questions, current category, and `success value`.

Sample:

```bash
curl api/v1/questions -X POST -H "Content-Type: application/json" -d '{
  "searchTerm":"who"
}'
```

```json
{
  "current_category": "all",
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": "4",
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know 
Why the Caged Bird Sings'?"
    },
    {
      "answer": "George Washington Carver",
      "category": "4",
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Alexander Fleming",
      "category": "1",
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Maya Angelou",
      "category": "4",
      "difficulty": 2,
      "id": 31,
      "question": "Whose autobiography is entitled 'I Know 
Why the Caged Bird Sings'?"
    },
    {
      "answer": "George Washington Carver",
      "category": "4",
      "difficulty": 2,
      "id": 38,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Alexander Fleming",
      "category": "1",
      "difficulty": 3,
      "id": 47,
      "question": "Who discovered penicillin?"
    }
  ],
  "success": true,
  "total_questions": 6
}
```

`POST 'api/v1/questions'`

* Post a new questions with the provded informations.
* Request Arguments: `dictionary of question info`
* Returns: A list of questions in group of 10 questions per page, number of total questions, category, success value.

Sample:

```bash
curl api/v1/questions -X POST -H "Content-Type: application/json" -d '{
  "question": "What is 2 + 7",
  "answer": 9,
  "category": 1,
  "difficulty": 3
}'
```

```json
{
  "current_category": "all",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": "5",
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": "5",
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"    
    },
    {
      "answer": "Maya Angelou",
      "category": "4",
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": "5",
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": "4",
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": "6",
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every 
soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": "6",
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": "4",
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": "3",
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"    
    },
    {
      "answer": "The Palace of Versailles",
      "category": "3",
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 45
}
```

`DELETE '/api/v1/questions/{question_id}'`

* Deletes a question with the given id
* Request Arguments: `question_id`
* Returns a `success value`

Sample:

```bash
curl '/api/v1/questions/45 -X DELETE
```

```json
{
  "success":true
}
```

`GET '/api/v1/categories/{category_id}/questions'`

* Fetch list of questions for a given category.
* Request Arguments: `category_id`
* Returns: A list of questions within a given category, number of total questions, current category and success value.

Sample:

```bash
curl /api/v1/categories/1/questions
```

```json
{
  "current_category": "Science",
  "questions": [
    {
      "answer": "The Liver",
      "category": "1",
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human 
body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": "1",
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": "1",
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "6",
      "category": "1",
      "difficulty": null,
      "id": 30,
      "question": "What is 1 + 5"
    },
    {
      "answer": "The Liver",
      "category": "1",
      "difficulty": 4,
      "id": 46,
      "question": "What is the heaviest organ in the human 
body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": "1",
      "difficulty": 3,
      "id": 47,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": "1",
      "difficulty": 4,
      "id": 48,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "9",
      "category": "1",
      "difficulty": null,
      "id": 50,
      "question": "What is 2 + 7"
    },
    {
      "answer": "9",
      "category": "1",
      "difficulty": null,
      "id": 51,
      "question": "What is 2 + 7"
    }
  ],
  "success": true,
  "total_questions": 9
}
```

[Goto Top](#backend---trivia-api)

## Error handling

We have handled five(5) common error type, when something went wrong. These are:

* _400_: Bad Request
* _404_: Not Found
* _405_: Method Not Allowed
* _422_: Unprocessable Entity
* _500_: Internal Server Error

Common errors are handled and return as JSON object in the following format:

```json
{
  "success": false,
  "message": "error name",
  "code": "error code"
}
```

Sample:

```bash
curl /api/v1/quizzes
```

```json
{
  "code": 405,
  "message": "Method Not Allowed",
  "success": false
}
```

[Goto Top](#backend---trivia-api)
