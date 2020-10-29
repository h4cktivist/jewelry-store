from datetime import datetime
import sys
import sqlite3 as lite
from flask import Flask, render_template, url_for, request, redirect, session, escape
from flask_sqlalchemy import SQLAlchemy
import telebot
from werkzeug.utils import secure_filename
from base64 import b64encode


app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

bot = telebot.TeleBot('1345360965:AAEljL8AmCV6pTK7TFd5SkoYZqrrizEGLSA')


class Feedback(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	feedback_name = db.Column(db.String(50), nullable=False)
	feedback_text = db.Column(db.String(150), nullable=False)
	date = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<Feedback %r>' % self.id


class NotificationInfo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	contact = db.Column(db.String(150), nullable=False)
	order = db.Column(db.String(150), nullable=False)

	def __repr__(self):
		return '<NotificationInfo %r>' % self.id


class NewProduct(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	product_name = db.Column(db.String(100), nullable=False)
	product_description = db.Column(db.String(200), nullable=False)
	product_date = db.Column(db.DateTime, default=datetime.utcnow)
	product_img = db.Column(db.BLOB())

	def __repr__(self):
		return '<NewProduct %r>' % self.id


def readImage(img_name):
	try:
		with open(img_name, 'rb') as file:
			img = file.stream.read()
		return img
	except IOError:
		print("ERROR!!")


@app.route('/admin_login', methods=['POST', 'GET'])
def admin_login():
	if request.method == 'POST':
		login = request.form['login']
		password = request.form['password']

		if not 'logged_in' in session:
			if (login == 'admin') and (password == 'admin_pass'):
				session['logged_in'] = True
				return redirect('/new_product_reg')
			else:
				return "Wrond login and passsword!"
		else:
			if 'logged_in' in session:
				return redirect('/new_product_reg')

	else:
		if 'logged_in' in session:
			return redirect('new_product_reg')

		return render_template('admin_login.html')


@app.route('/feedback', methods=['POST', 'GET'])
def feedback():
	if request.method == 'POST':
		feedback_name = request.form['feedback_name']
		feedback_text = request.form['feedback_text']

		feedback_data = Feedback(feedback_name=feedback_name, feedback_text=feedback_text)

		try:
			db.session.add(feedback_data)
			db.session.commit()
			return redirect('/feedback')
		except:
			return 'ERROR!'

	else:
		feedbacks = Feedback.query.order_by(Feedback.date.desc()).all()
		return render_template('feedback.html', feedbacks=feedbacks)


@app.route('/order', methods=['POST', 'GET'])
def order():
	if request.method == 'POST':
		name = request.form['name']
		contact = request.form['contact']
		order = request.form['order']

		notification_data = NotificationInfo(name=name, contact=contact, order=order)

		try:
			db.session.add(notification_data)
			db.session.commit()
			return redirect('/order')
		except:
			return 'ERROR!'

	else:
		return render_template('order.html')


@app.route('/new_product_reg', methods=['POST', 'GET'])
def new_product_reg():
	if request.method == 'POST':
		product_name = request.form['product_name']
		product_description = request.form['product_description']
		file = request.files['product_img']

		if file:
			img_name = secure_filename(file.filename)
			file.seek(0)
			product_img = file.read()
			product_img_binary = lite.Binary(product_img)

		product_data = NewProduct(product_name=product_name, product_description=product_description, product_img=product_img_binary)

		try:
			db.session.add(product_data)
			db.session.commit()
			return redirect('/new_product_reg')
		except:
			return "ERROR!"

	else:
		if 'logged_in' in session:
			return render_template('new_product_reg.html')
		else:
			return redirect('/admin_login')


@app.route('/products')
def products():
	products = NewProduct.query.order_by(NewProduct.product_date.desc()).all()
	for product in products:
		product.product_img = b64encode(product.product_img).decode('utf-8')
	return render_template('products.html', products=products)



@bot.message_handler(commands=['start'])
def start_message(message):
	notification = NotificationInfo.query.order_by(NotificationInfo.id.desc()).all()
	
	for el in notification:
		bot.send_message(message.chat.id, "Имя заказчика: " + el.name)
		bot.send_message(message.chat.id, "Как с ним связаться: " + el.contact)
		bot.send_message(message.chat.id, "Заказ: " + el.order)
		bot.send_message(message.chat.id, "_______________________________________")


if __name__ == "__main__":
	app.run(debug=True)
	bot.polling()
