from datetime import datetime
from example_db import example_mcq_questions, example_paragraph, example_paragraph_questions
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class MyQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(256), nullable=False)
    answer_1 = db.Column(db.String(256), nullable=False)
    answer_2 = db.Column(db.String(256), nullable=False)
    answer_3 = db.Column(db.String(256), nullable=False)
    answer_4 = db.Column(db.String(256), nullable=False)
    is_paragraph_question = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"Task {self.id}"


class ToggleState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    which_section = db.Column(db.String(20), nullable=False, default='mcq')


class MyParagraph(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paragraph = db.Column(db.String(2048), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)


def test_db(questions_count=10):
    # Check if data already exists
    if MyQuestion.query.first() or MyParagraph.query.first():
        print("Database already seeded. Skipping test_db()...")
        return  # Exit if data already exists

    counter = 1
    for question in example_mcq_questions[:questions_count]:
        db_entry = MyQuestion(question=str(counter) + '- ' + question[0], answer_1=question[1], answer_2=question[2], answer_3=question[3], answer_4=question[4], is_paragraph_question=False)
        db.session.add(db_entry)
        db.session.commit()
        counter += 1
    
    paragraph = MyParagraph(paragraph=example_paragraph)
    db.session.add(paragraph)
    db.session.commit()

    counter = 1
    for question in example_paragraph_questions[:questions_count]:
        db_entry = MyQuestion(question=str(counter) + '- ' + question[0], answer_1=question[1], answer_2=question[2], answer_3=question[3], answer_4=question[4], is_paragraph_question=True)
        db.session.add(db_entry)
        db.session.commit()
        counter += 1