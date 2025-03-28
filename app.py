from flask import Flask
from flask_scss import Scss
from src.models import db  # Import from models.py
import os


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "c194>gA.D0pC")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test_maker_database.db"

    db.init_app(app)
    Scss(app)

    with app.app_context():
        db.create_all()

    # Import and Register Blueprints
    from src.routes.main import main_bp
    from src.routes.auth import auth_bp
    from src.routes.questions import questions_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(questions_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
