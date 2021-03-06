from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextField, TextAreaField, SubmitField, FieldList, FormField, HiddenField
from wtforms.validators import InputRequired, Email, Length
from wtforms_components import DateField, TimeField

#TODO: do some research on WTForms-Components: https://wtforms-components.readthedocs.io/en/latest/#

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)], render_kw = {"placeholder": "email"})
    password = PasswordField('password', validators=[InputRequired(), Length(min=1, max=20)], render_kw = {"placeholder": "password"})
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
    organization_type = StringField('organization type')
    pick_up_method = StringField('pick up method')
    population = StringField('population')
    total_capacity = StringField('total capacity')
    current_inventory = StringField('current inventory')
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
    organization_type = StringField('organization type')
    pick_up_method = StringField('pick up method')
    population = StringField('population')
    total_capacity = StringField('total capacity')
    current_inventory = StringField('current inventory')

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
    organization_type = StringField('organization type')
    pick_up_method = StringField('pick up method')
    population = StringField('population')
    total_capacity = StringField('total capacity')
    current_inventory = StringField('current inventory')

class EditConsumerProfileForm(FlaskForm):
    name = StringField('name')
    address = StringField('current address')
    zip_code = StringField('zip code')
    city = StringField('city')
    state = StringField('state')
    country = StringField('country')
    phone = StringField('phone number')
    description = StringField('description')
    organization_type = StringField('organization type')
    pick_up_method = StringField('pick up method')
    population = StringField('population')
    total_capacity = StringField('total capacity')
    current_inventory = StringField('current inventory')

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
    organization_type = StringField('organization type')
    pick_up_method = StringField('pick up method')
    population = StringField('population')
    total_capacity = StringField('total capacity')
    current_inventory = StringField('current inventory')

class EditFoodbankProfileForm(FlaskForm):
    name = StringField('name')
    address = StringField('current address')
    zip_code = StringField('zip code')
    city = StringField('city')
    state = StringField('state')
    country = StringField('country')
    phone = StringField('phone number')
    description = StringField('description')
    organization_type = StringField('organization type')
    pick_up_method = StringField('pick up method')
    population = StringField('population')
    total_capacity = StringField('total capacity')
    current_inventory = StringField('current inventory')
    
# this is a subform for users to input food item information, can be used for DonateForm
class CategoryFoodForm(FlaskForm):
    category = SelectField('Select a category: ', choices=[('1', 'Category1'), ('2', 'Category2')])
    food_item = SelectField('Select a food item: ',
                            choices=[('1', 'foodItem1'), ('2', 'foodItem2'),
                                     ('3', 'foodItem3'), ('4', 'foodItem4'),('5', 'foodItem5'), ('6', 'foodItem6')])
    quantity = StringField("Quantity: ")
    weight = StringField("Weight: ")
    nutrition = StringField("Nutrition: ")
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

class ClaimForm(FlaskForm):
    claim_from = SelectField('Claim from: ', coerce=int)
    beneficiary = TextField("Perferred beneficiary (Optional): ")
    appointment_date = DateField('Appointment Date: ')
    appointment_time = TimeField('Appointment Time: ')
    frequency = SelectField('Frequency: ', choices=[('1', 'One Time'), ('2', 'Weekly'), ('3', 'Monthly')])
    notes = TextAreaField("Do you have anything specific for this consumption?")
    food_items = FieldList(FormField(CategoryFoodForm), min_entries=1) # subform for Category-Food
    plus_button = SubmitField("+")
    minus_button = SubmitField("-")
    def __init__(self, foodbank_choices):
        super(ClaimForm, self).__init__()
        self.claim_from.choices = foodbank_choices

class ManageDonateForm(FlaskForm):
    header_id = HiddenField()
    beneficiary = TextField("Perferred beneficiary (Optional): ")
    appointment_date = DateField('Appointment Date: ')
    appointment_time = TimeField('Appointment Time: ')
    frequency = SelectField('Frequency: ', choices=[('1', 'One Time'), ('2', 'Weekly'), ('3', 'Monthly')])
    notes = TextAreaField("Do you have anything specific for this donation?")
    food_items = FieldList(FormField(CategoryFoodForm), min_entries=1) # subform for Category-Food
    def __init__(self):
        super(ManageDonateForm, self).__init__()

class ManageClaimForm(FlaskForm):
    header_id = HiddenField()
    beneficiary = TextField("Perferred beneficiary (Optional): ")
    appointment_date = DateField('Appointment Date: ')
    appointment_time = TimeField('Appointment Time: ')
    frequency = SelectField('Frequency: ', choices=[('1', 'One Time'), ('2', 'Weekly'), ('3', 'Monthly')])
    notes = TextAreaField("Do you have anything specific for this consumption?")
    food_items = FieldList(FormField(CategoryFoodForm), min_entries=1) # subform for Category-Food
    def __init__(self):
        super(ManageClaimForm, self).__init__()

# Below is just for testing...
class LocationForm(FlaskForm):
    location_id = StringField('location_id')
    city = StringField('city')
class CompanyForm(FlaskForm):
    company_name = StringField('company_name')
    locations = FieldList(FormField(LocationForm), min_entries=2)
    plus_button = SubmitField("+")
    minus_button = SubmitField("-")



