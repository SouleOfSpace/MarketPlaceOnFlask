from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()

        if user:
            raise ValidationError('Username already exists! Please try a different username!')

    def validate_email_address(self, email_address_to_check):
        user = User.query.filter_by(email_address=email_address_to_check.data).first()

        if user:
            raise ValidationError('Email address already exists! Please try a different email address!')


    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password source:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Password repeat:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create account')


class LoginForm(FlaskForm):
    username = StringField(label='Your username:', validators=[DataRequired()])
    password = PasswordField(label='Your password:', validators=[DataRequired()])
    submit = SubmitField(label='Come in')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item!')

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item!')

class CreateItemForm(FlaskForm):
    name = StringField(label='Item name:', validators=[Length(max=30),DataRequired()])
    price = IntegerField(label='Item price ($):', validators=[DataRequired()])
    barcode = StringField(label='Item barcode:', validators=[Length(min=12, max=12), DataRequired()])
    description = StringField(label='Item description', validators=[Length(max=1024),DataRequired()])
    submit = SubmitField(label='Create item')

class DeleteITemForm(FlaskForm):
    submit = SubmitField(label='Delete')
