from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Model = declarative_base()


class Question(Model):
    """Question Model"""
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String(500), nullable=False, unique=True)
    answer = Column(String(150), nullable=False)
    difficulty = Column(Integer, nullable=False, default=3)
    category_id = Column(Integer, ForeignKey('categories.id'))

    def __init__(self, question, answer, category_id, difficulty):
        self.question = question
        self.answer = answer
        self.category_id = category_id
        self.difficulty = difficulty

    def __repr__(self):
        return f'<Question {self.id}>'

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category_id,
            'difficulty': self.difficulty
            }


class Category(Model):
    """Category Model"""
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False, unique=True)
    questions = relationship('Question', backref='category')

    def __init__(self, category_type: str):
        self.type = category_type
    
    def __repr__(self) -> str:
        return f'<Category {self.type}>'

    def format(self) -> dict:
        return {
            'id': self.id,
            'type': self.type
            }
