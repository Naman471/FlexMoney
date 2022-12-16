from ast import Pass
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, NumberRange, ValidationError
from Yoga_Centre.models import User, BatchDetails, Payment

class RegisterForm(FlaskForm):

    def validate_username(self,username_to_check):
        user=User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username Already Exists! Please try a different username')

    def validate_email(self,email_to_check):
        email=User.query.filter_by(email_address=email_to_check.data).first()
        if email:
            raise ValidationError('Email Address Already Exists! Please try a different email address')        
    
    username = StringField(label='User Name:', validators=[Length(min=2,max=30), DataRequired()])
    email = StringField(label='Email Address:', validators=[Email(),DataRequired()])
    password_1 = PasswordField(label='Password:', validators=[Length(min=5),DataRequired()])
    password_2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password_1'),DataRequired()])
    age = IntegerField(label='Age:',validators=[NumberRange(min=18,max=65),DataRequired()])
    month = StringField(label='Month',validators=[DataRequired()])
    batch_timing = SelectField(label='Batches', choices=['6-7 AM','7-8 AM','8-9 AM','5-6 PM'], validators=[DataRequired()])
    submit = SubmitField(label='Submit')

class BatchForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    month = StringField(label='Current Month',validators=[DataRequired()])
    new_batch_timing = SelectField(label='New Timing', choices=['6-7 AM','7-8 AM','8-9 AM','5-6 PM'], validators=[DataRequired()])
    submit = SubmitField(label='Make Changes')

class PaymentForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    month = StringField(label='Current Month',validators=[DataRequired()])
    submit = SubmitField(label='Make Payment')