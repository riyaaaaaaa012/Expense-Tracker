from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import session

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
    db.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app
