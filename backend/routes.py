from flask import Blueprint, jsonify, request, abort
from trivia_api import TriviaAPI
from trivia_functions import exists, get_int, format_questions

api = TriviaAPI()
route = Blueprint('route', __name__)


def setup_db(database_uri: str, questions_per_page: int):
    api.connect(database_uri, questions_per_page)
    return api.db


@route.route('/')
def index():
    return jsonify({
        'message': 'Welcome to Udacity Trivia API version 1.0.0.',
        'success': True
    })


@route.route("/categories")
def display_categories():
    """An endpoint to handle GET requests for all categories."""
    return jsonify({
        "success": True,
        "categories": exists(api.categories)
    })

 
@route.route('/questions', methods=['GET', 'POST'])
def display_questions():
    """
        An endpoint to handle GET requests for all questions.
        This endpoint return a list of questions per page,
        number of total questions, current category, categories.
        
        If the request method is POST, it checks if searchTerm is available.
        If it is available, it gets all questions based on the search term.
        It returns a list of questions per page for all questions for 
        whom the search term is a substring of.
        
        Or else it POSTs a new question to the database,
        which will require the question and answer text,
        category, and difficulty score.
    """
    questions_data = api.questions
    if request.method == 'POST':
        data = request.get_json()
        search_term = data.get("searchTerm", "")

        if search_term:
            questions_data = api.search(search_term)
        else:
            api.add_question(data)

    return format_questions(questions_data, api)

    
@route.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    """An endpoint to DELETE question using a question ID."""
    question_deleted = api.delete_question(get_int(question_id))

    if not question_deleted:
        abort(404)

    return jsonify({"success": True})


@route.route('/categories/<int:category_id>/questions')
def question_by_category(category_id):
    """A GET endpoint to get questions within a category."""
    questions_data = api.category_questions(get_int(category_id))
    
    return format_questions(questions_data, api)

    
@route.route("/quizzes", methods=["POST"])
def quiz():
    """
        A POST endpoint to get questions to play the quiz.
        This endpoint take category and previous question parameters
        and return a random questions within the given category,
        if provided, and that is not one of the previous questions.
    """

    data = request.get_json()

    if "quiz_category" not in data or "previous_questions" not in data:
        abort(422)

    category_id = data.get("quiz_category").get("id", 0)
    prev_questions = data.get("previous_questions", [])
    question = api.get_quiz_question(prev_questions, category_id)

    return jsonify({
        "success": True,
        "question": exists(question).format()
    })
