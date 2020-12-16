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
	date = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<Feedback %r>' % self.id


class ProductFeedback(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	fb_id = db.Column(db.Integer)
	user_name = db.Column(db.String, nullable=False)
	text = db.Column(db.String(200), nullable=False)
	date = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<ProductFeedback %r>' % self.id


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
	product_cost = db.Column(db.String(10), nullable=False)

	def __repr__(self):
		return '<NewProduct %r>' % self.id


def readImage(img_name):
	try:
		with open(img_name, 'rb') as file:
			img = file.stream.read()
		return img
	except IOError:
		print("ERROR!!")


@app.route('/')
def index():
	if not 'user_name' in session:
		return redirect('/user_login')
	else:
		return render_template('index.html')


@app.route('/registration', methods=['POST', 'GET'])
def registration():
	if request.method == 'POST':
		username = request.form['username']
		email = request.form['email']
		paswrd = request.form['paswrd']

		user_data = User(username=username, email=email, paswrd=paswrd)

		try:
			db.session.add(user_data)
			db.session.commit()
			return redirect('/user_login')
		except:
			return 'ERROR!'

	else:
		return render_template('registration.html')


@app.route('/user_login', methods=['POST', 'GET'])
def user_login():
	if request.method == 'POST':
		entered_username = request.form['username']
		entered_paswrd = request.form['paswrd']

		users = User.query.all()

		for user in users:
			if (entered_username == user.username) and (entered_paswrd == user.paswrd):
				session['user_name'] = user.username
				return redirect('/')
		else:
			return 'Неверный логин или пароль. Обновите страницу и повторите попытку'

	else:
		return render_template('user_login.html')


@app.route('/user_logout')
def logout():
	session['user_name'] = None
	return redirect('/')


@app.route('/admin_login', methods=['POST', 'GET'])
def admin_login():
	if request.method == 'POST':
		login = request.form['login']
		password = request.form['password']

		if not 'logged_in' in session:
			if (login == 'admin') and (password == 'admin_pass'):
				session['logged_in'] = True
				return redirect('/admin_page')
			else:
				return "Wrond login and passsword!"
		else:
			if 'logged_in' in session:
				return redirect('/admin_page')

	else:
		if 'logged_in' in session:
			return redirect('/admin_page')

		return render_template('admin_login.html')


@app.route('/admin_page')
def admin_page():
	if 'logged_in' in session:
		return render_template('admin_page.html')
	else:
		return redirect('/admin_login')


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


@app.route('/orders')
def orders():
	if 'logged_in' in session:
		orders = NotificationInfo.query.order_by(NotificationInfo.id.desc()).all()
		return render_template('orders.html', orders=orders)
	else:
		return redirect('/admin_login')


@app.route('/new_product_reg', methods=['POST', 'GET'])
def new_product_reg():
	if request.method == 'POST':
		product_name = request.form['product_name']
		product_description = request.form['product_description']
		product_cost = request.form['product_cost']
		file = request.files['product_img']

		if file:
			img_name = secure_filename(file.filename)
			file.seek(0)
			product_img = file.read()
			product_img_binary = lite.Binary(product_img)

		product_data = NewProduct(product_name=product_name, 
			product_description=product_description, 
			product_cost=product_cost, 
			product_img=product_img_binary)

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


@app.route('/products/<int:id>', methods=['POST', 'GET'])
def product_detail(id):
	if request.method == 'POST':
		fb_id = id
		user_name = session['user_name']
		text = request.form['text']

		product_feedbacks = ProductFeedback(fb_id=fb_id, user_name=user_name, text=text)

		try:
			db.session.add(product_feedbacks)
			db.session.commit()
			return redirect('/products')
		except:
			return 'ERROR!'

	if request.method == 'GET':
		product = NewProduct.query.get(id)
		feedbacks = ProductFeedback.query.order_by(ProductFeedback.date.desc()).all()
		product.product_img = b64encode(product.product_img).decode('utf-8')
		return render_template('product_detail.html', product=product, feedbacks=feedbacks)


@app.route('/cart', methods=['POST', 'GET'])
def cart():
	if 'cart' not in session:
		session['cart'] = []

	if request.method == 'POST':
		cart_prod_name = request.form['cart_prod_name']
		session['cart'].append(cart_prod_name)
		return redirect('/cart')

	if request.method == 'GET':
		cart_products = session['cart']
		return render_template('cart.html', cart_products=cart_products)


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
