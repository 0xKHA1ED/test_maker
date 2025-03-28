from flask import Blueprint, session, request, redirect

auth_bp = Blueprint("auth", __name__)


@auth_bp.before_request
def set_defaults():
    session.setdefault("username", "Khaled")
    session.setdefault("user-phone", "01016268099")
    session.setdefault("test-title", "Unit 7")


@auth_bp.route("/set", methods=["POST"])
def set_data():
    session["username"] = request.form['username']
    session["user-phone"] = request.form['user-phone']
    session["test-title"] = request.form['test-title']
    return redirect('/')