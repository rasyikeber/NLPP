from flask_wtf import FlaskForm
from wtforms.fields import DateField
from wtforms import TextAreaField,StringField,IntegerField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class DeptRegistrationForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    dpt_head_of = StringField('Department Head of', validators=[DataRequired()])    
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])    
    submit = SubmitField('Sign up')
class DeptLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember =BooleanField('Remember Me')
    submit = SubmitField('login')
class AddProject(FlaskForm):
    title = StringField('Student Project Idea Title', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Fill the project idea description/abstract', validators=[DataRequired()])
    dept = StringField('Department', validators=[DataRequired()]) 
    year = IntegerField('Graduation Year', validators=[DataRequired()]) 
    submission_date = DateField('Submission Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Add Project') 
