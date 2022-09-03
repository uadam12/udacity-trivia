from random import randint
import unittest
import json

from flaskr import create_app


def get_question():
    num1 = randint(1, 100)
    num2 = randint(1, 100)
    return {
        "question": f"What is {num1} + {num2}",
        "answer": num1 + num2,
        "category": 1,
        "difficulty": 3
    }


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    @classmethod
    def setUpClass(cls):
        """Define test variables and initialize app."""
        app = create_app(True)
        cls.client = app.test_client

    @classmethod
    def tearDownClass(cls):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        res = self.client().get('/api/v1/categories')
        data = json.loads(res.data)
        
        self.assertEqual(200, res.status_code)
        self.assertTrue(len(data['categories']) > 0)
        self.assertTrue(data['success'] is True)
        
    def test_get_categories_not_allowed_method(self):
        res = self.client().post('/api/v1/categories')
        data = json.loads(res.data)
        
        self.assertEqual(405, res.status_code)
        self.assertEqual(data['message'], 'Method Not Allowed')
        self.assertFalse(data['success'] is True)
        
    def test_get_question_per_page(self):
        res = self.client().get('/api/v1/questions')
        data = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertEqual(10, len(data['questions']))
        self.assertTrue(data['success'] is True)
        
    def test_get_page_page_not_found(self):
        res = self.client().get('/api/v1/questions?page=90')
        data = json.loads(res.data)
        
        self.assertEqual(404, res.status_code)
        self.assertEqual('Not Found', data['message'])
        self.assertFalse(data['success'] is True)
        
    def test_get_page_page_bad_request(self):
        res = self.client().get('/api/v1/questions?page=1000')
        data = json.loads(res.data)
        
        self.assertEqual(400, res.status_code)
        self.assertEqual('Bad Request', data['message'])
        self.assertFalse(data['success'] is True)
    
    def test_add_question(self):
        res = self.client().post("/api/v1/questions", json=get_question())
        data = json.loads(res.data)

        self.assertEqual(200, res.status_code)
        self.assertTrue(data['success'] is True)

    def test_delete_question(self):
        res = self.client().delete("/api/v1/questions/2")
        
        data = json.loads(res.data)
        self.assertEqual(200, res.status_code)
        self.assertTrue(data['success'] is True)
        
    def test_delete_question_not_found(self):
        res = self.client().delete("/api/v1/questions/1000")
        
        data = json.loads(res.data)
        self.assertEqual(404, res.status_code)
        self.assertEqual('Not Found', data['message'])
        self.assertFalse(data['success'] is True)
        
    def test_search_questions(self):
        term = "What"
        res = self.client().post("/api/v1/questions", json={"searchTerm": term})
        data = json.loads(res.data)
        questions = data['questions']
        term_is_substring_of_all_questions = \
            all(term.lower() in question["question"].lower() for question in questions)
        
        self.assertEqual(200, res.status_code)
        self.assertTrue(term_is_substring_of_all_questions is True)
        self.assertTrue(data['success'] is True)

    def test_search_questions_not_found(self):
        res = self.client().post("/api/v1/questions", json={"searchTerm": "BadSentenceABCDEFGHIJ"})
        
        data = json.loads(res.data)
        
        self.assertEqual(404, res.status_code)
        self.assertFalse(data['success'] is True)
        
    def test_get_questions_in_category(self):
        category = 3
        res = self.client().get(f'/api/v1/categories/{category}/questions')
        data = json.loads(res.data)
        questions = data['questions']
        questions_are_in_the_given_category = \
            all(category == int(question['category']) for question in questions)

        self.assertEqual(200, res.status_code)
        self.assertTrue(questions_are_in_the_given_category is True)
        self.assertTrue(data['success'] is True)
    
    def test_questions_not_found_in_category(self):
        res = self.client().get('/api/v1/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'] is True)
    
    def test_get_quiz_questions(self):
        category = {
            "id": 1,
            "type": ""
        }
        previous = []
        
        while True:
            res = self.client().post("/api/v1/quizzes", json={
                "quiz_category": category,
                "previous_questions": previous
            })
            data = json.loads(res.data)
            found = data['success']

            if not found:
                break

            question = data.get('question')
            question_id = int(question['id'])

            if category['id'] != 0:
                self.assertEqual(int(question['category']), category['id'])
            self.assertNotIn(question_id, previous)
            
            previous.append(question_id)

    def test_quiz_unprocessable_entity(self):
        res = self.client().post("/api/v1/quizzes", json={})
        data = json.loads(res.data)

        self.assertEqual(422, res.status_code)
        self.assertEqual('Unprocessable Entity', data['message'])
        self.assertFalse(data['success'] is True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
