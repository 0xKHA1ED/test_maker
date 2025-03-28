from flask import Blueprint, request, render_template, redirect, session
from src.models import db, MyQuestion, MyParagraph, ToggleState
from process_text import process_text


main_bp = Blueprint("main", __name__)


@main_bp.route('/', methods=['POST', 'GET'])
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
@main_bp.route('/toggle', methods=['POST'])
def toggle():
    selected_type = request.form.get("type")  # Get selected type (mcq or paragraph or paragraph-mcq)
    
    toggle_state = ToggleState.query.first()
    if not toggle_state:
        toggle_state = ToggleState(which_section='mcq')
        db.session.add(toggle_state)

    toggle_state.which_section = selected_type
    db.session.commit()

    return redirect('/')


@main_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    username = session["username"]
    phone_number = session["user-phone"]
    test_title = session["test-title"]

    return render_template(
            'settings.html',
            username=username,
            phone_number=phone_number,
            test_title=test_title)


@main_bp.route('/print_test', methods=['GET'])
def print_test():
    
    questions = MyQuestion.query.filter(MyQuestion.is_paragraph_question == False).order_by(MyQuestion.created).all()
    paragraphs = MyParagraph.query.order_by(MyParagraph.created).all()
    paragraph_questions = MyQuestion.query.filter(MyQuestion.is_paragraph_question == True).order_by(MyQuestion.created).all()
    
    return render_template('printable.html', questions=questions, paragraphs=paragraphs, paragraph_questions=paragraph_questions)