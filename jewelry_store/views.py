from flask import Blueprint, render_template, request, redirect, session, flash
from base64 import b64encode
import sqlite3 as lite
from werkzeug.utils import secure_filename

from jewelry_store import db
from .models import User, Product, ProductFeedback, Feedback, Order


views = Blueprint('views', __name__)

DB_ERROR_PAGE = 'error.html'
LOGIN_ERROR_PAGE = 'lg_error.html'


@views.route('/')
def index():
    products = Product.query.order_by(Product.product_date.desc()).all()
    for product in products:
        product.product_img = b64encode(product.product_img).decode('utf-8')
    return render_template('index.html', products=products)


@views.route('/registration', methods=['POST', 'GET'])
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
        except RuntimeError:
            return render_template(DB_ERROR_PAGE)

    else:
        return render_template('registration.html')


@views.route('/user_login', methods=['POST', 'GET'])
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
            return render_template(LOGIN_ERROR_PAGE)

    else:
        return render_template('user_login.html')


@views.route('/user_logout')
def logout():
    session['user_name'] = None
    return redirect('/')


@views.route('/admin/login', methods=['POST', 'GET'])
def admin_login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        if 'logged_in' not in session:
            if (login == 'admin') and (password == 'admin_pass'):
                session['logged_in'] = True
                return redirect('/admin')
            else:
                return render_template(LOGIN_ERROR_PAGE)
        else:
            if 'logged_in' in session:
                return redirect('/admin')

    else:
        if 'logged_in' in session:
            return redirect('/admin')

        return render_template('admin_login.html')


@views.route('/admin')
def admin_page():
    if 'logged_in' in session:
        return render_template('admin_page.html')
    else:
        return redirect('/admin/login')


@views.route('/admin/logout')
def admin_logout():
    session.pop('logged_in', None)
    return redirect('/admin/login')


@views.route('/feedback', methods=['POST', 'GET'])
def feedback():
    if request.method == 'POST':
        feedback_name = request.form['feedback_name']
        feedback_text = request.form['feedback_text']

        feedback_data = Feedback(feedback_name=feedback_name, feedback_text=feedback_text)

        try:
            db.session.add(feedback_data)
            db.session.commit()
            return redirect('/feedback')
        except RuntimeError:
            return render_template(DB_ERROR_PAGE)

    else:
        feedbacks = Feedback.query.order_by(Feedback.date.desc()).all()
        return render_template('feedback.html', feedbacks=feedbacks)


@views.route('/order', methods=['POST'])
def order():
    if request.method == 'POST':
        name = session['user_name']
        contact = request.form['contact']
        order = []

        for i in session['cart']:
            order.append(i['product_name'])

        order_info = Order(name=name, contact=contact, order=str(order))

        try:
            db.session.add(order_info)
            db.session.commit()
            session.pop('cart')
            flash('Ваш заказ был отправлен. С Вами скоро свяжется менеджер.')
            return redirect('/cart')
        except RuntimeError:
            return render_template(DB_ERROR_PAGE)


@views.route('/order_remove', methods=['POST'])
def order_remove():
    order_id = request.form['order_id']
    Order.query.filter_by(id=order_id).delete()
    db.session.commit()

    return redirect('/admin/orders')


@views.route('/admin/orders')
def orders():
    if 'logged_in' in session:
        orders = Order.query.order_by(Order.id.desc()).all()
        return render_template('orders.html', orders=orders)
    else:
        return redirect('/admin/login')


@views.route('/admin/new_product_reg', methods=['POST', 'GET'])
def new_product_reg():
    if request.method == 'POST':
        product_name = request.form['product_name']
        product_description = request.form['product_description']
        product_cost = request.form['product_cost']
        product_category = request.form['category']
        file = request.files['product_img']

        if file:
            secure_filename(file.filename)
            file.seek(0)
            product_img = file.read()
            product_img_binary = lite.Binary(product_img)

        product_data = Product(product_name=product_name,
                               product_description=product_description,
                               product_cost=product_cost,
                               product_category=product_category,
                               product_img=product_img_binary)

        try:
            db.session.add(product_data)
            db.session.commit()
            return redirect('/admin/new_product_reg')
        except RuntimeError:
            return render_template(DB_ERROR_PAGE)

    else:
        if 'logged_in' in session:
            return render_template('new_product_reg.html')
        else:
            return redirect('/admin/login')


@views.route('/products', methods=['POST', 'GET'])
def products():
    if request.method == 'POST':
        product_category = request.form['category']
        products = Product.query.filter_by(product_category=product_category).all()
        for product in products:
            product.product_img = b64encode(product.product_img).decode('utf-8')
        return render_template('index.html', products=products)

    if request.method == 'GET':
        products = Product.query.order_by(Product.product_date.desc()).all()
        for product in products:
            product.product_img = b64encode(product.product_img).decode('utf-8')
        return render_template('index.html', products=products)


@views.route('/products/<int:id>', methods=['POST', 'GET'])
def product_detail(id):
    if request.method == 'POST':
        fb_id = id
        user_name = session['user_name']
        text = request.form['text']
        image = request.files['image']

        if image:
            secure_filename(image.filename)
            image.seek(0)
            image = image.read()
            image = lite.Binary(image)

            product_feedbacks = ProductFeedback(fb_id=fb_id, user_name=user_name, text=text, image=image)

        else:
            product_feedbacks = ProductFeedback(fb_id=fb_id, user_name=user_name, text=text)

        try:
            db.session.add(product_feedbacks)
            db.session.commit()
            return redirect('/')
        except RuntimeError:
            return render_template(DB_ERROR_PAGE)

    if request.method == 'GET':
        product = Product.query.get(id)
        feedbacks = ProductFeedback.query.order_by(ProductFeedback.date.desc()).all()

        product.product_img = b64encode(product.product_img).decode('utf-8')

        for feedback in feedbacks:
            if feedback.image:
                feedback.image = b64encode(feedback.image).decode('utf-8')
            else:
                pass

        return render_template('product_detail.html', product=product, feedbacks=feedbacks)


@views.route('/cart', methods=['POST', 'GET'])
def cart():
    if 'user_name' not in session:
        return redirect('/user_login')

    else:
        if 'cart' not in session:
            session['cart'] = []

        if request.method == 'POST':
            session['cart'] += [{
                'product_name': request.form['product_name'],
                'product_cost': request.form['product_cost'],
                'product_img': request.form['product_img'],
            }]

            return redirect('/cart')

        if request.method == 'GET':
            cart_products = session['cart']
            full_cost = sum([float(x['product_cost']) for x in session['cart']])

            return render_template('cart.html', cart_products=cart_products, full_cost=full_cost)


@views.route('/cart_clear')
def cart_clear():
    session.pop('cart')
    return redirect('/cart')


@views.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404
