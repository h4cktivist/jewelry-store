from datetime import datetime
from . import db


CURRENT_TIME = datetime.now()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    paswrd = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feedback_name = db.Column(db.String(50), nullable=False)
    feedback_text = db.Column(db.String(150), nullable=False)
    date = db.Column(db.String, default=CURRENT_TIME.strftime("%d-%m-%Y %H:%M"))

    def __repr__(self):
        return '<Feedback %r>' % self.id


class ProductFeedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fb_id = db.Column(db.Integer)
    user_name = db.Column(db.String, nullable=False)
    text = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String, default=CURRENT_TIME.strftime("%d-%m-%Y %H:%M"))
    image = db.Column(db.BLOB())

    def __repr__(self):
        return '<ProductFeedback %r>' % self.id


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(150), nullable=False)
    order = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return '<Order %r>' % self.id


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    product_description = db.Column(db.String(200), nullable=False)
    product_date = db.Column(db.String, default=CURRENT_TIME.strftime("%d-%m-%Y %H:%M"))
    product_img = db.Column(db.BLOB())
    product_category = db.Column(db.String(30), nullable=False)
    product_cost = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<Product %r>' % self.id
