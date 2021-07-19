from os import path

from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret_key'
    app.config['SESSION_TYPE'] = 'filesystem'
    Session().init_app(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from jewelry_store.views import views

    app.register_blueprint(views, url_prefix='/')

    from .models import User, Product, ProductFeedback, Feedback, Order

    create_db(app)

    return app


def create_db(app):
    if not path.exists('jewelry_store/database.db'):
        db.create_all(app=app)
        print(' * SQLite Database Created')
