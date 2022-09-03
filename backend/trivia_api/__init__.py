from random import choice
from .crud import TriviaCRUD
from .models import Question, Category


class TriviaAPI:
    def __init__(self, database_uri: str = None, questions_per_page: int = None):
        """Constructor of Trivia API that will handle database connectivity.
        Args:
            database_uri(str): database connection uri
            questions_per_page(int): number of question per single page.
        """
        if database_uri is not None:
            self.connect(database_uri, questions_per_page)
        else:
            self.db = None
            self.__questions_per_page = 10

    def connect(self, database_uri: str, questions_per_page: int):
        self.db = TriviaCRUD(database_uri)

        if type(questions_per_page) != int or questions_per_page < 1:
            self.__questions_per_page = 10
        elif questions_per_page > 50:
            self.__questions_per_page = 50
        else:
            self.__questions_per_page = questions_per_page

    @property
    def categories(self) -> dict:
        return dict([(category.id, category.type) for category in self.db.all(Category)])

    @property
    def questions(self) -> dict:
        return {
            "questions": [question.format() for question in self.db.all(Question)],
            "category": "All"
        }

    def category_questions(self, category_id: int) -> dict:
        category = self.db.get(Category, category_id)

        if category_id == 0:
            return self.questions

        if category is not None:
            return {
                "questions": [question.format() for question in category.questions],
                "category": category.type
            }

        return {}

    def paginated_questions(self, questions: list, page_number: int = 1) -> list:
        """ Paginate the given questions list in group of questions_per_page (example 10 questions per page).
        Parameter(s):
            page_number(int): number of page,
            questions(list): list of questions to
        Returns: List of questions per single page.
        """
        start = (page_number - 1) * self.__questions_per_page
        end = start + self.__questions_per_page

        if not questions:
            return []

        return questions[start:end]

    def search(self, term: str) -> dict:
        """
        Parameter:
            term (str): given search term.
        Returns: questions of which search term is substring of.
        """
        questions = self.db.session.query(Question).filter(Question.question.ilike(f"%{term}%")).all()
        return {
            "questions": [question.format() for question in questions],
            "category": "All"
        }

    def get_quiz_question(self, prev_question_ids: list, category_id: int) -> Question | None:
        """ Select a random unanswered question for quiz,
        Args:
            prev_question_ids (list): List of ids of previously answered questions
            category_id: id of category of the current questions
        Returns:
            Question: an unanswered question
        """

        category_questions = self.category_questions(category_id)
        questions = set([question.get('id') for question in category_questions.get("questions")])
        prev_questions = set(prev_question_ids)
        next_question_ids = list(questions - prev_questions)

        if not next_question_ids:
            return None

        next_question_id = choice(next_question_ids)

        return self.db.get(Question, next_question_id)

    def delete_question(self, question_id: int):
        """Delete a question from the database.
        Args:
            question_id(int): id of the question to be deleted.
        """
        return self.db.delete(Question, question_id)

    def add_question(self, data: dict):
        """Add a new question to the database.
        Args:
            data(dict): information of the question to be added.
        """
        self.db.add(Question(
            data.get("question"),
            data.get("answer"),
            data.get("category"),
            data.get("difficulty")
        ))
