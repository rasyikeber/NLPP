from flask import render_template, flash, redirect, url_for,request
from nlp.advisor.forms import   AdvRegistrationForm,AdvLoginForm
from  nlp.models import Student, Adviser, Newproject

from flask_login import login_user, current_user, logout_user, login_required
from nlp import db, bcrypt
from functools import wraps


from flask import Blueprint


def advisor_required(f):
    @wraps(f)
    def adv_decorated_function(*args, **kwargs):
        # Check if the current user is authenticated and is a department head
        if not current_user.is_authenticated or not current_user.is_adviser:
            # Redirect the user to the login page or display an error message
            flash('You are not authorized to access this page.', 'danger')
            return redirect(url_for('advisors.adv_login'))
        return f(*args, **kwargs)
    return adv_decorated_function

advisors= Blueprint('advisors',__name__)

@advisors.route('/adv-signup',methods=['GET', 'POST'])
def adv_signup():
  if current_user.is_authenticated:
    return redirect(url_for('advisors.adv_home'))
  form =AdvRegistrationForm()
  if form.validate_on_submit():
    hashed_password =bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    adv = Adviser(name=form.name.data, email=form.email.data, dpt=form.advdpt.data,special_in=form.special.data, password=hashed_password)
    db.session.add(adv)
    db.session.commit()
    flash(f'your account has been created!', 'success')
    return redirect(url_for('advisors.adv_login'))
  return render_template('adv-signup.html', title= "adv sign up", form=form)

@advisors.route('/adv-login', methods=['GET', 'POST'])
def adv_login():
  form = AdvLoginForm()
  if current_user.is_authenticated and current_user.is_adviser:
    return redirect(url_for('advisors.adv_home'))  # Redirect to the index page if user is already logged in
  else:
     if form.validate_on_submit():
        advsor = Adviser.query.filter_by(email=form.email.data).first()
        if advsor and bcrypt.check_password_hash(advsor.password, form.password.data):
          login_user(advsor, remember=form.remember.data)
          next_page = request.args.get('next')
          return redirect(next_page) if next_page else redirect(url_for('advisors.adv_home'))
        else:
           flash('Login Unsuccessful. Please check student ID and password.', 'danger')

  return render_template('adv-login.html', title='adv Login', form=form)

@advisors.route('/adv-logout')
@login_required
@advisor_required
def adv_logout():
  logout_user()
  return redirect(url_for('advisors.adv_login'))

@advisors.route('/adv-home', methods=['GET', 'POST'])
@login_required
@advisor_required
def adv_home():
     # Retrieve projects where the current user is the adviser
    projects=Newproject.query.filter_by(adviser_name=current_user.name).all()
    print(f" {current_user.name} projects ",projects)
    # Create a dictionary to store project and related students
    projects_with_students = {}
    # Iterate through project
    for project in projects:
        # Retrieve students related to the current project's group_id
        students = Student.query.filter_by(group_id=project.group_id).all()
        # Add the project and related students to the dictionary
        projects_with_students[project] = students
    # Render the template with the projects and related students
    return render_template('adv-home.html', projects_with_students=projects_with_students)
  