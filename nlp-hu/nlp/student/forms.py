from flask_wtf import FlaskForm
from wtforms.fields import DateField
from wtforms import TextAreaField,StringField,IntegerField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from nlp.models import Student
import re

class RegistrationForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    studid = IntegerField('Student ID',validators=[DataRequired()])  
    dpt = StringField('Department', validators=[DataRequired()])    
    year = IntegerField('Graduation Year', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])    
    submit = SubmitField('Sign up')

    def validate_ID(self, studid):
       user = Student.query.filter_by(studid=studid.data).first()
       if user:
          raise ValidationError('This ID is already taken')

    
    def validate_email(self, email):
        user =Student.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('this email already taken  ')
    
    def validate_password(self, password):
        if not (len(password.data) >= 4 and re.search("[!@#$%^&*()-_+=]", password.data)):
            raise ValidationError('Password must be at least 4 characters long and contain at least one special character.')
    def validate_confirm_password(self, confirm_password):
        if self.password.data != confirm_password.data:
            raise ValidationError('Passwords must match.')

class LoginForm(FlaskForm):
    studid = IntegerField('Student ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember =BooleanField('Remember Me')
    submit =SubmitField('Login')


''' submit project idea forms'''
class SubmitProject(FlaskForm):
    title = StringField('Project Idea Title', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Fill your project idea description/abstract', validators=[DataRequired()])
    dept = StringField('Your Department', validators=[DataRequired()]) 
    year = IntegerField('Graduate Year', validators=[DataRequired()]) 
    submission_date = DateField('Submission Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')