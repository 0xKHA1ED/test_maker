from flask import Blueprint

main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
questions_bp = Blueprint('questions', __name__)