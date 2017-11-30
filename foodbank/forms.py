from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextField, TextAreaField, SubmitField, FieldList, FormField
from wtforms.validators import InputRequired, Email, Length
from wtforms_components import DateField, TimeField

#TODO: do some research on WTForms-Components: https://wtforms-components.readthedocs.io/en/latest/#

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=1, max=20)])
    remember = BooleanField('remember me')

class RegisterDonorForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])
    name = StringField('name')
    address = StringField('current address')
    zip_code = StringField('zip code')
    city = StringField('city')
    state = StringField('state')
    country = StringField('country')
    phone = StringField('phone number')
    description = StringField('description')
    #add app.config['RECAPTCHA_PUBLIC_KEY'] app.config['RECAPTCHA_PRIVATE_KEY']
    # do not forget to add {{ form.recaptcha }} in templates
    #recaptcha = RecaptchaFeild()

class EditDonorProfileForm(FlaskForm):
    name = StringField('name')
    address = StringField('current address')
    zip_code = StringField('zip code')
    city = StringField('city')
    state = StringField('state')
    country = StringField('country')
    phone = StringField('phone number')
    description = StringField('description')
    # add app.config['RECAPTCHA_PUBLIC_KEY'] app.config['RECAPTCHA_PRIVATE_KEY']
    # do not forget to add {{ form.recaptcha }} in templates
    # recaptcha = RecaptchaFeild()

class RegisterConsumerForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])
    name = StringField('name')
    address = StringField('current address')
    zip_code = StringField('zip code')
    city = StringField('city')
    state = StringField('state')
    country = StringField('country')
    phone = StringField('phone number')
    description = StringField('description')

class RegisterFoodbankForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])
    name = StringField('name')
    address = StringField('current address')
    zip_code = StringField('zip code')
    city = StringField('city')
    state = StringField('state')
    country = StringField('country')
    phone = StringField('phone number')
    description = StringField('description')

# this is a subform for users to input food item information, can be used for DonateForm
class CategoryFoodForm(FlaskForm):
    category = SelectField('Select a category: ', choices=[('1', 'Category1'), ('2', 'Category2')])
    food_item = SelectField('Select a food item: ', choices=[('1', 'foodItem1'), ('2', 'foodItem2')])
    quantity = StringField("Quantity: ")
    weight = StringField("weight: ")
    expiration_date = DateField('Expiration Date: ')

class DonateForm(FlaskForm):
    donate_to = SelectField('Donate to: ', coerce=int)
    beneficiary = TextField("Perferred beneficiary (Optional): ")
    appointment_date = DateField('Appointment Date: ')
    appointment_time = TimeField('Appointment Time: ')
    frequency = SelectField('Frequency: ', choices=[('1', 'One Time'), ('2', 'Weekly'), ('3', 'Monthly')])
    notes = TextAreaField("Do you have anything specific for this donation?")
    food_items = FieldList(FormField(CategoryFoodForm), min_entries=1) # subform for Category-Food
    plus_button = SubmitField("+")
    minus_button = SubmitField("-")
    def __init__(self, foodbank_choices):
        super(DonateForm, self).__init__()
        self.donate_to.choices = foodbank_choices

class ManageForm(FlaskForm):
    beneficiary = TextField("Perferred beneficiary (Optional): ")
    appointment_date = DateField('Appointment Date: ')
    appointment_time = TimeField('Appointment Time: ')
    frequency = SelectField('Frequency: ', choices=[('1', 'One Time'), ('2', 'Weekly'), ('3', 'Monthly')])
    notes = TextAreaField("Do you have anything specific for this donation?")
    food_items = FieldList(FormField(CategoryFoodForm), min_entries=1) # subform for Category-Food
    plus_button = SubmitField("+")
    minus_button = SubmitField("-")
    def __init__(self, donation_header, donation_detail):
        super(ManageForm, self).__init__()
        self.beneficiary.data = donation_header.beneficiary
        # self.appointment_date.data = donation_header.appointment_date
        self.appointment_time.data = donation_header.appointment_time
        self.frequency.data = donation_header.frequency
        self.notes.data = donation_header.notes
        for x in range(1, len(donation_detail)):
            self.food_items.append_entry()
        for x in range(0, len(donation_detail)):
            self.food_items.__getitem__(x).category.data = donation_detail[x].category_id
            self.food_items.__getitem__(x).food_item.data = donation_detail[x].food_item_id
            self.food_items.__getitem__(x).quantity.data = donation_detail[x].quantity
            self.food_items.__getitem__(x).weight.data = donation_detail[x].weight
            # self.food_items.__getitem__(x).expiration_date.data = donation_detail[x].expiration_date

# Below is just for testing...
class LocationForm(FlaskForm):
    location_id = StringField('location_id')
    city = StringField('city')
class CompanyForm(FlaskForm):
    company_name = StringField('company_name')
    locations = FieldList(FormField(LocationForm), min_entries=2)
    plus_button = SubmitField("+")
    minus_button = SubmitField("-")



