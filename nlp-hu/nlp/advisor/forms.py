from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class AdvRegistrationForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    advdpt = StringField(' You Department', validators=[DataRequired()]) 
    special = StringField('Speciality in', validators=[DataRequired()]) 
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])    
    submit = SubmitField('Sign up')
class AdvLoginForm(FlaskForm):
    email = StringField('Advisor Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember =BooleanField('Remember Me')
    submit = SubmitField('login')

