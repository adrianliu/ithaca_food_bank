from flask import Flask, render_template, redirect, url_for, flash
import os
from flask import request

from flask_bootstrap import Bootstrap
from flask_sqlalchemy  import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import LoginForm, RegisterDonorForm, RegisterConsumerForm, RegisterFoodbankForm, DonateForm, CompanyForm, ManageForm, EditDonorProfileForm, ViewForm
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
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(20))
    name = db.Column(db.String(50))
    address = db.Column(db.String(50))
    zip_code = db.Column(db.String(50))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    country = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    description = db.Column(db.String(50))
    # organization_type = db.Column(db.String(50))
    user_type = db.Column(db.Integer)
    # pick_up_method = db.Column(db.String(50))
    # population = db.Column(db.String(50))
    # total_capacity = db.Column(db.String(50))
    # current_inventory = db.Column(db.String(50))

class RequestHeader(db.Model):
    __tablename__ = 'request_header'
    id = db.Column(db.Integer, primary_key=True)
    from_user = db.Column(db.Integer, ForeignKey("user.id"), nullable=False) #reference to User(id)
    to_user = db.Column(db.Integer, ForeignKey("user.id"), nullable=False) #reference to User(id)
    appointment_date = db.Column(db.Date)
    appointment_time = db.Column(db.Time)
    request_type = db.Column(db.Integer) # either donation request or claim request
    beneficiary = db.Column(db.String(50))
    frequency = db.Column(db.Integer) # 1: One Time; 2. Weekly; 3. Monthly
    notes = db.Column(db.String(500))
    status = db.Column(db.Integer) # 0: pending; 1: approved
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    request_details = relationship('RequestDetail', backref='request_header', lazy='dynamic')

class RequestDetail(db.Model):
    __tablename__ = 'request_detail'
    id = db.Column(db.Integer, primary_key=True)
    request_header_id = db.Column(db.Integer, ForeignKey("request_header.id"), nullable=False) # reference to RequestHeader(id)
    food_item_id = db.Column(db.Integer, ForeignKey("food_item.id"), nullable=False) # reference to FoodItem(id)
    category_id = db.Column(db.Integer, ForeignKey("category.id"), nullable=False) # reference to Category(id)
    quantity = db.Column(db.String(50))
    weight = db.Column(db.String(50))
    expiration_date = db.Column(db.String(50))
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class TransactionHeader(db.Model):
    __tablename__ = 'transaction_header'
    id = db.Column(db.Integer, primary_key=True)
    from_user = db.Column(db.Integer, ForeignKey("user.id"), nullable=False) #reference to User(id)
    to_user = db.Column(db.Integer, ForeignKey("user.id"), nullable=False) #reference to User(id)
    appointment_date = db.Column(db.Date)
    appointment_time = db.Column(db.Time)
    transaction_type = db.Column(db.Integer) # either donation transaction or claim transaction
    beneficiary = db.Column(db.String(50))
    frequency = db.Column(db.Integer) # 1: One Time; 2. Weekly; 3. Monthly
    notes = db.Column(db.String(500))
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class TransactionDetail(db.Model):
    __tablename__ = 'transaction_detail'
    id = db.Column(db.Integer, primary_key=True)
    transaction_header_id = db.Column(db.Integer, ForeignKey("transaction_header.id"), nullable=False) # reference to RequestHeader(id)
    food_item_id = db.Column(db.Integer, ForeignKey("food_item.id"), nullable=False) # reference to FoodItem(id)
    category_id = db.Column(db.Integer, ForeignKey("category.id"), nullable=False) # reference to Category(id)
    quantity = db.Column(db.String(50))
    weight = db.Column(db.String(50))
    expiration_date = db.Column(db.String(50))
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class FoodItem(db.Model):
    __tablename__ = 'food_item'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, ForeignKey("category.id"), nullable=False) #reference to Category(id)
    name = db.Column(db.String(50))
    description = db.Column(db.String(500))
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(500))
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    food_items = relationship('FoodItem', backref='category', lazy='dynamic')

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
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid email or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup/donor', methods=['GET', 'POST'])
def signup_donor():
    form = RegisterDonorForm()

    if form.validate_on_submit():
        email_exists = db.session.query(User.id).filter_by(email=form.email.data).scalar() is not None

        if email_exists:
            return 'Email address already existed!'
        else:
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = User(
                email = form.email.data, 
                password = hashed_password,
                name = form.name.data,
                address = form.address.data,
                zip_code = form.zip_code.data,
                city = form.city.data,
                state = form.state.data,
                country = form.country.data,
                phone = form.phone.data,
                description = form.description.data,
                user_type = TYPE_DONOR)

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
        email_exists = db.session.query(User.id).filter_by(email=form.email.data).scalar() is not None

        if email_exists:
            return 'Email address already existed!'
        else:
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = User(
                email = form.email.data, 
                password = hashed_password,
                name = form.name.data,
                address = form.address.data,
                zip_code = form.zip_code.data,
                city = form.city.data,
                state = form.state.data,
                country = form.country.data,
                phone = form.phone.data,
                description = form.description.data,
                user_type = TYPE_CONSUMER)
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
        email_exists = db.session.query(User.id).filter_by(email=form.email.data).scalar() is not None

        if email_exists:
            return 'Email address already existed!'
        else:
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = User(
                email = form.email.data, 
                password = hashed_password,
                name = form.name.data,
                address = form.address.data,
                zip_code = form.zip_code.data,
                city = form.city.data,
                state = form.state.data,
                country = form.country.data,
                phone = form.phone.data,
                description = form.description.data,
                user_type = TYPE_FOODBANK)
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
    foodbanks = db.session.query(User.id, User.name).filter_by(user_type = TYPE_FOODBANK).all()

    categories = db.session.query(Category).all()
    categories = Category.query.all()
    # load all of the category->food mapping to memory
    category_food_dict = {}
    for category in categories:
        food_items = category.food_items.all()
        category_food_dict[str(category.id)] = food_items
    print '------------category_food_dict----------------'
    print category_food_dict
    form = DonateForm(foodbank_choices=foodbanks)
    # form = DonateForm()
    if form.plus_button.data:
        form.food_items.append_entry()
    elif form.minus_button.data:
        form.food_items.pop_entry()
    elif form.validate_on_submit():#post successfully
        # insert the donation request into database
        new_request_header = RequestHeader(
            from_user = current_user.id,
            to_user = int(form.donate_to.data),
            appointment_date = form.appointment_date.data,
            appointment_time = form.appointment_time.data,
            request_type = REQUEST_DONATION,
            beneficiary = form.beneficiary.data,
            frequency = form.frequency.data,
            notes = form.notes.data,
            status = REQUEST_PENDING)

        db.session.add(new_request_header)
        db.session.commit()

        for entry in form.food_items.entries:
            new_request_detail = RequestDetail(
                request_header_id=new_request_header.id,
                food_item_id=entry.data['food_item'],
                category_id=entry.data['category'],
                quantity=entry.data['quantity'],
                weight=entry.data['weight'],
                expiration_date=entry.data['expiration_date']
            )
            db.session.add(new_request_detail)

        db.session.commit()
        flash("You have successfully submitted a donation request!")
        return redirect(url_for('dashboard'))

    return render_template('donate_request.html', donateForm=form, user=current_user)

@app.route('/manage/donation', methods=['GET', 'POST'])
@login_required
def manage_donation():
    donation_request = db.session.query(RequestHeader, User)\
        .filter_by(to_user = current_user.id, request_type = REQUEST_DONATION, status = REQUEST_PENDING)\
        .join(User, RequestHeader.from_user == User.id).all()
    donation_transaction = db.session.query(TransactionHeader, User).filter_by(to_user = current_user.id, transaction_type = REQUEST_DONATION).join(User, TransactionHeader.from_user == User.id).all()
    return render_template('manage_donation.html', head_id = current_user.id, donation_request = donation_request, donation_transaction = donation_transaction)

@app.route('/manage/donation/edit/<donation_id>', methods=['GET', 'POST'])
@login_required
def edit_donation(donation_id):
    donation_header = db.session.query(RequestHeader).filter_by(id = donation_id).first()
    donation_detail = db.session.query(RequestDetail).filter_by(request_header_id = donation_id).all()  
    form = ManageForm()
    if request.method == 'POST':
        if form.plus_button.data:
            form.food_items.append_entry()
        elif form.minus_button.data:
            form.food_items.pop_entry()
        elif form.validate_on_submit():
            if request.form['submit'] == 'Update':
                donation_header.beneficiary = form.beneficiary.data
                donation_header.appointment_date = form.appointment_date.data
                donation_header.appointment_time = form.appointment_time.data
                donation_header.frequency = form.frequency.data
                donation_header.notes = form.notes.data
                db.session.query(RequestDetail).filter_by(request_header_id = donation_id).delete()
                for entry in form.food_items.entries:
                    new_request_detail = RequestDetail(
                        request_header_id=donation_id,
                        food_item_id=entry.data['food_item'],
                        category_id=entry.data['category'],
                        quantity=entry.data['quantity'],
                        weight=entry.data['weight'],
                        expiration_date=entry.data['expiration_date']
                    )
                    db.session.add(new_request_detail)
                db.session.commit()
                flash('You have updated one request!')
                return redirect(url_for('dashboard'))
            elif request.form['submit'] == 'Approve':
                donation_header.status = REQUEST_APPROVED
                new_transaction_header = TransactionHeader(
                    id = donation_id,
                    from_user = donation_header.from_user,
                    to_user = donation_header.to_user,
                    appointment_date = form.appointment_date.data,
                    appointment_time = form.appointment_time.data,
                    transaction_type = REQUEST_DONATION,
                    beneficiary = form.beneficiary.data,
                    frequency = form.frequency.data,
                    notes = form.notes.data)
                db.session.add(new_transaction_header)
                db.session.commit()

                for entry in form.food_items.entries:
                    new_transaction_detail = TransactionDetail(
                        transaction_header_id=new_transaction_header.id,
                        food_item_id=entry.data['food_item'],
                        category_id=entry.data['category'],
                        quantity=entry.data['quantity'],
                        weight=entry.data['weight'],
                        expiration_date=entry.data['expiration_date']
                    )
                    db.session.add(new_transaction_detail)
                db.session.commit()
                flash('You have approved one transaction!')
                return redirect(url_for('dashboard'))
    else:
        form.header_id.data = donation_header.id
        form.beneficiary.data = donation_header.beneficiary
        form.appointment_date.data = donation_header.appointment_date
        form.appointment_time.data = donation_header.appointment_time
        form.frequency.choice = donation_header.frequency
        form.notes.data = donation_header.notes
        for x in range(1, len(donation_detail)):
            form.food_items.append_entry()
        for x in range(0, len(donation_detail)):
            form.food_items.__getitem__(x).category.data = donation_detail[x].category_id
            form.food_items.__getitem__(x).food_item.data = donation_detail[x].food_item_id
            form.food_items.__getitem__(x).quantity.data = donation_detail[x].quantity
            form.food_items.__getitem__(x).weight.data = donation_detail[x].weight
            print '-----------------'
            print type(donation_detail[x].expiration_date)
            print donation_detail[x].expiration_date
            form.food_items.__getitem__(x).expiration_date.data = \
                datetime.strptime(donation_detail[x].expiration_date, '%Y-%m-%d')
    return render_template('edit_donation.html', donateForm = form)   

@app.route('/manage/donation/view/<donation_id>', methods=['GET'])
@login_required
def view_donation(donation_id):
    donation_header = db.session.query(TransactionHeader).filter_by(id = donation_id).first()
    donation_detail = db.session.query(TransactionDetail).filter_by(transaction_header_id = donation_id).all()  
    return render_template('view_donation.html', donation_header = donation_header, donation_detail = donation_detail)

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

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = current_user
    form = EditDonorProfileForm()
    if form.validate_on_submit():
        user.name = form.name.data
        user.address = form.address.data
        user.zip_code = form.zip_code.data
        user.city = form.city.data
        user.state = form.state.data
        user.country = form.country.data
        user.phone = form.phone.data
        user.description = form.description.data
        db.session.commit()
        flash('Your profile has been updated!')
        return redirect(url_for('dashboard'))
    else:
        form.name.data = user.name
        form.address.data = user.address
        form.zip_code.data = user.zip_code
        form.city.data = user.city
        form.state.data = user.state
        form.country.data = user.country
        form.phone.data = user.phone
        form.description.data = user.description
    return render_template('edit_profile.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/test', methods=['GET', 'POST'])
def test():
    form = CompanyForm(request.form)
    if form.plus_button.data:
        form.locations.append_entry()
    elif form.minus_button.data:
        form.locations.pop_entry()
    elif form.validate_on_submit():
        print request.form['company_name']
        print len(form.locations.entries)
        for entry in form.locations.entries:
            print entry.data['location_id']
            print entry.data['city']
        return 'test form submitted!'
    print(form.errors)
    return render_template('test_field_list.html', companyForm=form)
