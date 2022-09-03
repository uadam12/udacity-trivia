from flask import Flask, jsonify
from flask_cors import CORS
from .config import DATABASE_URI, TEST_DATABASE_URI
from routes import route, setup_db

QUESTIONS_PER_PAGE = 10


def create_app(test=False):
    # create and configure the app
    app = Flask(__name__)
    database_uri = TEST_DATABASE_URI if test else DATABASE_URI
    app.db = setup_db(database_uri, QUESTIONS_PER_PAGE)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    app.register_blueprint(route, url_prefix="/api/v1")

    @app.after_request
    def after_request(res):
        res.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authentication, true')
        res.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
        
        return res
    
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Welcome to Udacity Trivia API.',
            'success': True
        })
    
    """
    @TODO:
        Create error handlers for all expected errors
        including 404 and 422.
    """
    @app.errorhandler(400)
    @app.errorhandler(404)
    @app.errorhandler(405)
    @app.errorhandler(422)
    @app.errorhandler(500)
    def handle_common_errors(e):
        return jsonify({
            'success': False,
            "message": e.name,
            "code": e.code
        }), e.code

    return app
