from flask import Blueprint, jsonify, json, request
from api import API
from flaskr import QUESTIONS_PER_PAGE

api = API(QUESTIONS_PER_PAGE)
route = Blueprint('route', __name__)

def page_number():
    return request.args.get("page", 1, int)

@route.route("/categories")
def categories():
    """
        An endpoint to handle GET requests
        for all available categories.
    """
    return jsonify({
        "success":True,
        "categories": api.exists(api.categories)
    })
 
    
"""
@TODO:
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.

@TODO:
    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    
@TODO:
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
"""

@route.route('/questions', methods=['GET', 'POST'])
def questions():
    """
        An endpoint to handle GET requests for all questions.
        This endpoint return a list of questions per page,
        number of total questions, current category, categories.
        
        If the request method is POST, it check wether searchTerm is available.
        If searchTerm available, it get all questions based on a search term.
        It returns a list of questions per page for all questions for 
        whom the search term is a substring of.
        
        Or else it POST a new question,
        which will require the question and answer text,
        category, and difficulty score.
    """
    questions = api.all_questions()
    if request.method == 'POST':
        data = request.get_json()
        searchTerm = data.get("searchTerm", "")

        if searchTerm:
            questions = api.search(searchTerm)
        else:
            api.add_question(data)
            return jsonify({"success": True})
    
    return jsonify({
        "success": True,
        "questions": api.exists(api.questions_per_page(questions, page_number())),
        "total_questions": len(questions),
        "current_category": api.current_category
    })
    
"""
@TODO:

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
"""
@route.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    """An endpoint to DELETE question using a question ID."""
    api.delete_question(question_id)
    return jsonify({"success": True})


"""
@TODO:
    

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
"""
@route.route('/categories/<int:category_id>/questions')
def question_by_category(category_id):
    """A GET endpoint to get questions within a category."""
    questions = api.exists(api.questions_in_category(category_id))
    
    return jsonify({
        "success": True,
        "questions": api.exists(api.questions_per_page(questions, page_number())),
        "total_questions": len(questions),
        "current_category": api.current_category
    }) 
    
"""
@TODO:
    

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
"""
@route.route("/quizzes", methods=["POST"])
def quiz():
    """
        A POST endpoint to get questions to play the quiz.
        This endpoint take category and previous question parameters
        and return a random questions within the given category,
        if provided, and that is not one of the previous questions.
    """

    data = request.get_json()
    category_id = data.get("quiz_category").get("id", 0)
    prev_questions = data.get("previous_questions", [])
    question = api.exists(api.quiz_question(prev_questions, category_id))

    return jsonify({
        "success":True,
        "question":question.format()
    })