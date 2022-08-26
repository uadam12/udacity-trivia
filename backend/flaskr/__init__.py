from flask import Flask, jsonify
from flask_cors import CORS

from models import setup_db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/api/*":{"origins":"*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    from routes import route
    app.register_blueprint(route, url_prefix="/api/v1")
    
    @app.after_request
    def after_request(res):
        res.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authentication, true')
        res.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
        
        return res
    
    
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
            'success':False,
            "message": e.name,
            "code": e.code
        }), e.code

    return app

