from flask_wtf import FlaskForm
from wtforms.fields import DateField
from wtforms import TextAreaField,StringField,IntegerField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError,NumberRange
from nlp.models import Student
import re

class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    studid = IntegerField('Student ID', validators=[
        DataRequired(),
        NumberRange(min=1000, max=9999, message="ID must be a 4-digit number")
    ])
   
    

    dpt = StringField('Department', validators=[
        DataRequired(),
        Length(max=3, message="must be Two character")                                        ])    
    year = IntegerField('Graduation Year', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(max=8, message="password must be 8 digits")
        ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password'),
        Length(max=8, message="password must be 8 digits")
        
        ])    
    submit = SubmitField('Sign up')

    
    
    def validate_ID(self, studid):
       user = Student.query.filter_by(studid=studid.data).first()
       if user:
          raise ValidationError('This ID is already taken')
    def validate_email(self, email):
        if '@' and '.' not in email.data:
            raise ValidationError('Invalid email address. Must contain . and @  .')
        user = Student.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already taken')
    def validate_password(self, password):
        if not (len(password.data) > 8 and re.search("[!@#$%^&*()-_+=]", password.data)):
            raise ValidationError('Password must be at least 8 characters long and contain at least one special character.')
    def validate_confirm_password(self, confirm_password):
        if self.password.data != confirm_password.data:
            raise ValidationError('Passwords must match.')
        
   
class LoginForm(FlaskForm):
    studid = IntegerField('Student ID', validators=[
       DataRequired(),
       Length(max=8, message="password must be 8 digits")                                              
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(max=8, message="password must be 8 digits")                                              
    ])
    remember =BooleanField('Remember Me')
    submit =SubmitField('Login')


''' submit project idea forms'''
class SubmitProject(FlaskForm):
    title = StringField('Project Idea Title', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Write Down your project idea description/abstract', validators=[DataRequired()])
    dept = StringField('Your Department', validators=[DataRequired()]) 
    year = IntegerField('Graduate Year', validators=[DataRequired()]) 
    submission_date = DateField('Submission Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')