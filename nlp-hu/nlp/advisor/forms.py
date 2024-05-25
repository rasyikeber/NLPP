from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class AdvRegistrationForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    advdpt = StringField(' You Department', validators=[
        DataRequired(),
        Length(max=3, message="password must be 8 digits")                                              
                                         ]) 
    special = StringField('Speciality in', validators=[DataRequired(),Length(min=20, max=80)]) 
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


 
class AdvLoginForm(FlaskForm):
    email = StringField('Advisor Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(max=8, message="password must be 8 digits")])
    remember =BooleanField('Remember Me')
    submit = SubmitField('login')

