from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, length, ValidationError
from principal.models import User


class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    button_submit = SubmitField('Login')


class FormRegistro(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), length(min=6), length(max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    button_submit = SubmitField('Register')

    def validate_email(self, email):
        username = User.query.filter_by(email=email.data).first()
        if username:
            return ValidationError('Email already registered. Please use a different email.')
