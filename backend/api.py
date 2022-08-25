import random
from flask import abort
from models import Question, Category

class API:
    def validate_int(self, num: int):
        if type(num) != int:
            abort(400)
            
        return num
    
    def validate_page(self, page: int):
        if self.validate_int(page) > 100:
            abort(400)
            
        return page
    
    def exists(self, obj):
        if not obj:
            abort(404)
            
        return obj

    # categories
    @property
    def categories(self) -> dict:
        return self.__categories
    
    # current_category
    @property
    def current_category(self) -> str:
        return self.__current_category
        
    # constructor    
    def __init__(self, questions_per_page: int):
        """
            Construct to an API that will take care of maninfulating information from database.
        Args:
            questions_per_page (int): Number of question per single page.
        """
        
        if type(questions_per_page) != int or questions_per_page < 1:
            self.__questions_per_page = 10
        elif questions_per_page > 50:
            self.__questions_per_page = 50
        else:
            self.__questions_per_page = questions_per_page

        self.__current_category = 'all'
        self.__categories = dict([(category.id, category.type) for category in Category.query.all()])
    
    def all_questions(self):
        return Question.query.order_by(Question.id).all()
    
    def questions_in_category(self, category_id):
        category = Category.query.get(self.validate_int(category_id))
        
        if category:
            return Question.query.filter_by(category = category.id).order_by(Question.id).all()
        else:
            return []
    
    def questions_per_page(self, questions: list, page_number: int = 1) -> int:
        """
        Parameter(s):
            page_number(int): number of page
        Returns:
            int: Questions per single page.
        """    
        page = self.validate_page(page_number)
        start = (page - 1) * self.__questions_per_page
        end = start + self.__questions_per_page
        
        return [question.format() for question in questions[start:end]]
    
    def quiz_question(self, prev_question_ids: list, category_id: int) -> Question:
        """
            Pick a random question for quiz, 
            if question's id is not in previous questions.
        Args:
            prev_question_ids (list): List of ids of previously answerd quetions
            category_id: id of the given category
        Returns:
            Question: an unanswered question
        """
        
        category = Category.query.get(self.validate_int(category_id))
        if category:
            questions = set([q.id for q in self.questions_in_category(category.id)])
        else:
            questions = set([q.id for q in self.all_questions()])

        prev_questions = set(prev_question_ids)
        next_question_ids = list(questions - prev_questions)
        next_question_id = random.choice(next_question_ids)
        
        return Question.query.get(next_question_id)
    
    
    def search(self, term:str):
        """
            Search question based on the given term.
        Args:
            term (str): a term to search for.
        Returns: questions of which term is substring of.
        """
        return Question.query.filter(
            Question.question.ilike(f"%{term}%")
        ).order_by(Question.id).all()
    
    def delete_question(self, question_id: int):
        """
            Delete a question from the database.
        Args:
            question_id (int): id of the question to be deleted.
        """

        self.exists(
            Question.query.get(self.validate_int(question_id))
        ).delete()
        
    def add_question(self, data: dict):
        """
            Add a new quetion to the database.
        Args:
            data (dict): information of the quetion to be added.
        """
        Question(
            data.get("question"),
            data.get("answer"),
            data.get("category"),
            data.get("diffculity")
        ).insert()