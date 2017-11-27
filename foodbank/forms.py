from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

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
    #add app.config['RECAPTCHA_PUBLIC_KEY'] app.config['RECAPTCHA_PRIVATE_KEY']
    # do not forget to add {{ form.recaptcha }} in templates
    #recaptcha = RecaptchaFeild()

class RegisterFoodbankForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    #add app.config['RECAPTCHA_PUBLIC_KEY'] app.config['RECAPTCHA_PRIVATE_KEY']
    # do not forget to add {{ form.recaptcha }} in templates
    #recaptcha = RecaptchaFeild()
