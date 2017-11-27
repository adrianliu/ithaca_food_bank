from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Email, Length

#TODO: do some research on WTForms-Components: https://wtforms-components.readthedocs.io/en/latest/#

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterDonorForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    #add app.config['RECAPTCHA_PUBLIC_KEY'] app.config['RECAPTCHA_PRIVATE_KEY']
    # do not forget to add {{ form.recaptcha }} in templates
    #recaptcha = RecaptchaFeild()

class RegisterConsumerForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class RegisterFoodbankForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class DonateForm(FlaskForm):
    donate_to = SelectField('Donate to: ', choices = [('foodbank1', 'foodbank1'), ('foodbank2', 'foodbank2')])
    beneficiary = TextField("Perferred beneficiary (Optional): ")
    frequency = SelectField('Frequency: ', choices = [('1','One Time'), ('2','Weekly'), ('3','Monthly')])
    appointment_date = TextField('Appointment Date: ')
    notes = TextAreaField("Do you have anything specific for this donation?")
    submit = SubmitField('Make a Donation')

