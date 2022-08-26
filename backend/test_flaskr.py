import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        #self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        # I prefer in memory database for test
        self.database_path = "sqlite:///trivia_test.db"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    
    def test_get_categories(self):
        res = self.client().get('/api/v1/categories')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['success'])
        
    def test_get_categories_not_allowed_method(self):
        res = self.client().post('/api/v1/categories')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['message'], 'Method Not Allowed')
        self.assertFalse(data['success'])
        
    def test_get_question_per_page(self):
        res = self.client().get('/api/v1/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['questions']), 10)
        self.assertTrue(data['success'])
        
    def test_get_page_page_not_found(self):
        res = self.client().get('/api/v1/questions?page=90')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Not Found')
        self.assertFalse(data['success'])
        
    def test_get_page_page_bad_request(self):
        res = self.client().get('/api/v1/questions?page=1000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], 'Bad Request')
        self.assertFalse(data['success'])
    
    def test_add_question(self):
        question_info = {
            "question": "What is 5 + 3",
            "answer": 8,
            "category": 1,
            "difficulty": 3
        }
        res = self.client().post("/api/v1/questions", json=question_info)
        
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
    
    def test_delete_question(self):
        res = self.client().delete("/api/v1/questions/24")
        
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        
    def test_delete_question_not_found(self):
        res = self.client().delete("/api/v1/questions/1000")
        
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], 'Not Found')
        self.assertFalse(data['success'])
        
    def test_search_questions(self):
        term = "What"
        res = self.client().post("/api/v1/questions", json={"searchTerm": term})
        data = json.loads(res.data)
        questions = data['questions']
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(all(term.lower() in q["question"].lower() for q in questions))
        
    def test_search_questions_not_found(self):
        res = self.client().post("/api/v1/questions", json={"searchTerm": "BadSentenceABCDEFGHIJ"})
        
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        
    def test_get_questions_in_category(self):
        category = 3
        res = self.client().get(f'/api/v1/categories/{category}/questions')
        data = json.loads(res.data)
        
        questions = data['questions']
        
        self.assertTrue(all(category == int(q['category']) for q in questions))
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
    
    def test_get_questions_in_category_not_found(self):
        res = self.client().get('/api/v1/categories/1000/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
    
    def test_get_quiz_question(self):
        quiz = {
            "quiz_category":{
                "id":0,
                "type":"all"
            },
            "previous_questions":[2, 3, 4, 5, 6, 7, 8]
        }
        res = self.client().post("/api/v1/quizzes", json=quiz)
        data = json.loads(res.data)
        category = data['question']['category']
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertNotIn(category, quiz["previous_questions"])

    def test_quiz_unprocessable_entity(self):
        quiz = {}
        res = self.client().post("/api/v1/quizzes", json=quiz)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'Unprocessable Entity')
        self.assertFalse(data['success'])
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()