from flask import Flask, render_template, redirect, request, session
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from process_text import process_text
from example_db import example_mcq_questions, example_paragraph, example_paragraph_questions

# App
app = Flask(__name__)
app.secret_key = "c194>gA.D0pC"


@app.before_request
def set_defaults():
    if "username" not in session:
        session["username"] = "Khaled"
    if "user-phone" not in session:
        session["user-phone"] = "01016268099"
    if "test-title" not in session:
        session["test-title"] = "Unit 7"


@app.route("/set", methods=["POST"])
def set_data():
    session["username"] = request.form['username']
    session["user-phone"] = request.form['user-phone']
    session["test-title"] = request.form['test-title']

    return redirect('/')


Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test_maker_database.db"
db = SQLAlchemy(app)


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


@app.route('/', methods=['POST', 'GET'])
def index():
    # Add a question
    if request.method == 'POST':
        text = request.form['content']
        question, answers = process_text(text)[0], process_text(text)[1]
        answer_1, answer_2, answer_3, answer_4 = answers[0], answers[1], answers[2], answers[3]
        test_question = MyQuestion(question=question, answer_1=answer_1, answer_2=answer_2, answer_3=answer_3, answer_4=answer_4)
        try:
            db.session.add(test_question)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR: {e}"
    # See all current tasks
    else:
        # Fetch toggle state from the database
        toggle_state = ToggleState.query.first()
        which_section = toggle_state.which_section if toggle_state else 'mcq'

        questions = MyQuestion.query.filter(MyQuestion.is_paragraph_question == False).order_by(MyQuestion.created).all()
        paragraphs = MyParagraph.query.order_by(MyParagraph.created).all()
        paragraph_questions = MyQuestion.query.filter(MyQuestion.is_paragraph_question == True).order_by(MyQuestion.created).all()
        
        return render_template('index.html', questions=questions, section=which_section, paragraphs=paragraphs, paragraph_questions=paragraph_questions)


# Switch between MCQ or Paragraph
@app.route('/toggle', methods=['POST'])
def toggle():
    selected_type = request.form.get("type")  # Get selected type (mcq or paragraph or paragraph-mcq)
    
    toggle_state = ToggleState.query.first()
    if not toggle_state:
        toggle_state = ToggleState(which_section='mcq')
        db.session.add(toggle_state)

    toggle_state.which_section = selected_type
    db.session.commit()

    return redirect('/')


# Delete an item
@app.route('/delete/<int:id>')
def delete(id: int):
    delete_task = MyQuestion.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"ERROR: {e}"


# Edit an item
@app.route('/edit/<int:id>', methods=["GET", "POST"])
def edit(id: int):
    task = MyQuestion.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"ERROR: {e}"
    else:
        return render_template("edit.html", task=task)


@app.route('/add_paragraph', methods=['POST'])
def add_paragraph():
    content = request.form['paragraph-content']
    paragraph_text = MyParagraph(paragraph=content)
    db.session.add(paragraph_text)
    db.session.commit()
    return redirect('/')


@app.route('/add_paragraph_question', methods=['POST'])
def add_paragraph_question():
    content = request.form['content']
    question, answers = process_text(content)[0], process_text(content)[1]
    answer_1, answer_2, answer_3, answer_4 = answers[0], answers[1], answers[2], answers[3]
    question = MyQuestion(question=question, answer_1=answer_1, answer_2=answer_2, answer_3=answer_3, answer_4=answer_4, is_paragraph_question=True)
    db.session.add(question)
    db.session.commit()
    return redirect('/')


@app.route('/print_test', methods=['GET'])
def print_test():
    
    questions = MyQuestion.query.filter(MyQuestion.is_paragraph_question == False).order_by(MyQuestion.created).all()
    paragraphs = MyParagraph.query.order_by(MyParagraph.created).all()
    paragraph_questions = MyQuestion.query.filter(MyQuestion.is_paragraph_question == True).order_by(MyQuestion.created).all()
    
    return render_template('printable.html', questions=questions, paragraphs=paragraphs, paragraph_questions=paragraph_questions)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    username = session["username"]
    phone_number = session["user-phone"]
    test_title = session["test-title"]

    return render_template(
            'settings.html',
            username=username,
            phone_number=phone_number,
            test_title=test_title)


@app.route('/delete_all', methods=['POST'])
def delete_all():
    questions = MyQuestion.query.all()
    paragraphs = MyParagraph.query.all()

    for question in questions:
        db.session.delete(question)
    
    for paragraph in paragraphs:
        db.session.delete(paragraph)
    
    db.session.commit()

    return redirect('/')


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


if __name__ in '__main__':
    with app.app_context():
        db.create_all()
        test_db(20)
    app.run(debug=True)