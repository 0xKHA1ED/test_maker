from flask import request, redirect, Blueprint, render_template
from src.models import db, MyQuestion, MyParagraph
from process_text import process_text


questions_bp = Blueprint("questions", __name__)


@questions_bp.route('/add_paragraph', methods=['POST'])
def add_paragraph():
    content = request.form['paragraph-content']
    paragraph_text = MyParagraph(paragraph=content)
    db.session.add(paragraph_text)
    db.session.commit()
    return redirect('/')


@questions_bp.route('/add_paragraph_question', methods=['POST'])
def add_paragraph_question():
    content = request.form['content']
    question, answers = process_text(content)[0], process_text(content)[1]
    answer_1, answer_2, answer_3, answer_4 = answers[0], answers[1], answers[2], answers[3]
    question = MyQuestion(question=question, answer_1=answer_1, answer_2=answer_2, answer_3=answer_3, answer_4=answer_4, is_paragraph_question=True)
    db.session.add(question)
    db.session.commit()
    return redirect('/')


# Delete an item
@questions_bp.route('/delete/<int:id>')
def delete(id: int):
    delete_task = MyQuestion.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"ERROR: {e}"


# Edit an item
@questions_bp.route('/edit/<int:id>', methods=["GET", "POST"])
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


@questions_bp.route('/delete_all', methods=['POST'])
def delete_all():
    questions = MyQuestion.query.all()
    paragraphs = MyParagraph.query.all()

    for question in questions:
        db.session.delete(question)
    
    for paragraph in paragraphs:
        db.session.delete(paragraph)
    
    db.session.commit()

    return redirect('/')