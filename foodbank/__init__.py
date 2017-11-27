from flask import Flask, render_template, redirect, url_for, flash
import os

from flask_bootstrap import Bootstrap
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import LoginForm, RegisterDonorForm, RegisterConsumerForm, RegisterFoodbankForm, DonateForm
from datetime import datetime


TYPE_FOODBANK = 0
TYPE_DONOR = 1
TYPE_CONSUMER = 2

REQUEST_DONATION = 1
REQUEST_CONSUMPTION = 2

REQUEST_PENDING = 0
REQUEST_APPROVED = 1

# App instance
app = Flask(__name__)
app.config.from_object('config.Config')

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ------------------- Models -----------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    user_type = db.Column(db.Integer)

class RequestHeader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    form_user = db.Column(db.Integer) #reference to User(id)
    to_user = db.Column(db.Integer) #reference to User(id)
    appointment_date = db.Column(db.String(50))
    appointment_time = db.Column(db.String(50))
    request_type = db.Column(db.Integer) # either donation request or claim request
    beneficiary = db.Column(db.String(50))
    frequency = db.Column(db.Integer) # 1: One Time; 2. Weekly; 3. Monthly
    notes = db.Column(db.String(500))
    status = db.Column(db.Integer) # 0: pending; 1: approved
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class RequestDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_header_id = db.Column(db.Integer) # reference to RequestHeader(id)
    food_item_id = db.Column(db.Integer) # reference to FoodItem(id)
    category_id = db.Column(db.Integer) # reference to Category(id)
    quantity = db.Column(db.String(50))
    weight = db.Column(db.String(50))
    expiration_date = db.Column(db.String(50))
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer) #reference to Category(id)
    name = db.Column(db.String(50))
    description = db.Column(db.String(500))
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(500))
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@app.errorhandler(404)
def not_found(error):
  return render_template('404.html'), 404

# Set up user_loader 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ------------------- Routes, acting as Controllers -----------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup/donor', methods=['GET', 'POST'])
def signup_donor():
    form = RegisterDonorForm()

    if form.validate_on_submit():
        username_exists = db.session.query(User.id).filter_by(username=form.username.data).scalar() is not None
        email_exists = db.session.query(User.id).filter_by(email=form.email.data).scalar() is not None

        if username_exists or email_exists:
        	return 'Username or Email already existed!'
        else:
        	hashed_password = generate_password_hash(form.password.data, method='sha256')
        	new_user = User(
        		username=form.username.data, 
        		email=form.email.data, 
        		password=hashed_password,
        		user_type=TYPE_DONOR)

        	# add new user to the database
        	db.session.add(new_user)
        	db.session.commit()

        	flash('You have been signed up as a Donor!')
        	# redirect to the login page
        	return redirect(url_for('login'))
        	#return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup_donor.html', form=form)

@app.route('/signup/consumer', methods=['GET', 'POST'])
def signup_consumer():
    form = RegisterConsumerForm()

    if form.validate_on_submit():
        username_exists = db.session.query(User.id).filter_by(username=form.username.data).scalar() is not None
        email_exists = db.session.query(User.id).filter_by(email=form.email.data).scalar() is not None

        if username_exists or email_exists:
        	return 'Username or Email already existed!'
        else:
        	hashed_password = generate_password_hash(form.password.data, method='sha256')
        	new_user = User(
        		username=form.username.data, 
        		email=form.email.data, 
        		password=hashed_password,
        		user_type=TYPE_CONSUMER)
        	# add new user to the database
        	db.session.add(new_user)
        	db.session.commit()

        	flash('You have been signed up as a Consumer!')
        	# redirect to the login page
        	return redirect(url_for('login'))
        	#return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup_consumer.html', form=form)

@app.route('/signup/foodbank', methods=['GET', 'POST'])
def signup_foodbank():
    form = RegisterFoodbankForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(
        	username=form.username.data, 
        	email=form.email.data, 
        	password=hashed_password,
        	user_type=TYPE_FOODBANK)

        username_exists = db.session.query(User.id).filter_by(username=form.username.data).scalar() is not None
        email_exists = db.session.query(User.id).filter_by(email=form.email.data).scalar() is not None

        if username_exists or email_exists:
        	return 'Username or Email already existed!'
        else:
        	# add new user to the database
        	db.session.add(new_user)
        	db.session.commit()

        	flash('You have been signed up as a Foodbank!')
        	# redirect to the login page
        	return redirect(url_for('login'))
        	#return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'


    return render_template('signup_foodbank.html', form=form)

# For donors to make a donation
@app.route('/donate', methods=['GET', 'POST'])
@login_required
def donate():
    form = DonateForm()
    if form.validate_on_submit():
        return 'You have successfully submitted a donation request!'

    return render_template('donate_request.html', form=form, user=current_user)


@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.user_type == TYPE_FOODBANK:
        return render_template('dashboard_foodbank.html', user=current_user)
    elif current_user.user_type == TYPE_DONOR:
        return render_template('dashboard_donor.html', user=current_user)
    elif current_user.user_type == TYPE_CONSUMER:
        return render_template('dashboard_consumer.html', user=current_user)
    else:
    	# direct the user to the index page if something wrong happened
		return index()

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

