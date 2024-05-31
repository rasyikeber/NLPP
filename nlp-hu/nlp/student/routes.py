from flask import render_template, flash,Blueprint, redirect, url_for,request,session,jsonify
from nlp.student.forms import RegistrationForm, LoginForm, SubmitProject
from nlp.student.utils import check_similarity_with_projects
from  nlp.models import Student,Newproject,Oldproject,Adviser
import random,time



from flask_login import login_user, current_user, logout_user, login_required
from nlp import  db, bcrypt
from functools import wraps

student= Blueprint('student',__name__)
def student_required(f):
    @wraps(f)
    def stud_decorated_function(*args, **kwargs):
        # Check if the current user is authenticated and is a department head
        if not current_user.is_authenticated or not current_user.is_student:
            # Redirect the user to the login page or display an error message
            flash('You are not authorized to access this page.', 'danger')
            return redirect(url_for('student.login'))
        return f(*args, **kwargs)
    return stud_decorated_function

def generate_group_id(department):
    timestamp = str(int(time.time()))  # Get current timestamp as a string
    random_number = str(random.randint(1, 100))  # Generate a random number
    group_id = department + timestamp + random_number  # Concatenate department, timestamp, and random number
    return group_id



@student.route('/registre', methods=['GET','POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('student.home'))
  form =RegistrationForm()
  if form.validate_on_submit():
        # Check if studid already exists
    student = Student.query.filter_by(studid=form.studid.data).first()
    if student:
      flash('Student ID already exists.', 'error')
      return render_template('signup.html', title="Student Sign Up", form=form)
        
    # If studid is unique, proceed with registration
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    stud = Student(name=form.name.data, email=form.email.data, studid=form.studid.data, dpt=form.dpt.data, year=form.year.data, password=hashed_password)
    db.session.add(stud)
    db.session.commit()
    
    flash('Your account has been created!', 'success')
    return redirect(url_for('student.login'))
    
  return render_template('signup.html', title="Student Sign Up", form=form)

@student.route('/')
@student.route('/loginuser',methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if current_user.is_authenticated and current_user.is_student:
    return redirect(url_for('student.home'))
  else:
     if form.validate_on_submit():
        stud = Student.query.filter_by(studid=form.studid.data).first()
        if stud and bcrypt.check_password_hash(stud.password, form.password.data):
          login_user(stud, remember=form.remember.data)
          next_page = request.args.get('next')
          return redirect(next_page) if next_page else redirect(url_for('student.home'))
        else:
           flash('Login Unsuccessful. Please check student ID and password.', 'danger')

  return render_template('login.html', title='student Login', form=form)



@student.route('/home', methods=['GET', 'POST'])
@login_required
@student_required
def home():
    # retrieve data from student table
    currentUser = Student.query.filter_by(id=current_user.id).first()
    groupID = currentUser.group_id
    #print(currentUser.name)
    
    userProject = Newproject.query.filter_by(group_id=groupID).all()
    adv = []
    if len(userProject)==1:
       adv= Adviser.query.filter_by(name=userProject[0].adviser_name).first()
    else:
       print("no adviser")
    groupStud = []
    if groupID or userProject:
        groupStud = Student.query.filter_by(group_id=groupID).all()
    else:
        flash("You do not have any project available and not grouped yet", 'danger')

    return render_template('home.html', title='Home Page',
                           currentUser=currentUser,
                           groupStud=groupStud,
                           userProject=userProject,
                           adv=adv
                           )

@student.route('/group',methods=['GET','POST'])
@login_required
@student_required
def form_group():
  if request.method == 'POST':
    idno1 = request.form.get('idno1')
    idno2 = request.form.get('idno2')
    print(idno1,idno2)
    curnt_stud =Student.query.filter_by(id=current_user.id).first()
    if curnt_stud.is_grouped:
      flash("you already in a group",'danger')
      return redirect(url_for('student.home'))
    elif curnt_stud.is_student:
      group_id = generate_group_id(current_user.dpt)
      print()
      print(idno1,idno2, group_id)
      stud1 = Student.query.filter_by(studid=idno1).first()
      stud2 = Student.query.filter_by(studid=idno2).first()
      # update the group id and the is_grouped column
      curnt_stud.update_isgrpd_status_and_gr_id(True, group_id)
      stud1.update_isgrpd_status_and_gr_id(True, group_id)
      stud2.update_isgrpd_status_and_gr_id(True, group_id)
      flash(f"Group created successfully: {curnt_stud.name}, {stud1.name}, {stud2.name}",category='success')
      return redirect(url_for("student.home"))
    else:
      flash("something went wrong")
    
  return render_template('form-group.html', title='create group')


@student.route('/submit-projectidea',methods=['GET','POST'])
@login_required
@student_required
def submit_projectidea():
    form = SubmitProject()
    currentUser = Student.query.filter_by(id=current_user.id).first()
    if currentUser.is_grouped and currentUser.is_student:
        if form.validate_on_submit():
            title = form.title.data
            description = form.description.data
            date = form.submission_date.data
            project = Newproject(title=title, description=description, group_id=currentUser.group_id, pdpt=currentUser.dpt, year=currentUser.year, date=date, adviser_name=None, is_approved=False)
            similarity_threshold = 0.70 
            project_count = session.get(f'project_count_{current_user.id}', 0)

            similarity_found = check_similarity_with_projects(title, description, [Newproject.query.first()], similarity_threshold, 'New')
            if not similarity_found:
                similarity_found = check_similarity_with_projects(title, description, [Oldproject.query.first()], similarity_threshold, 'Last year')
                if not similarity_found: 
                    try:
                        db.session.add(project)
                        db.session.commit()
                        project_count += 1
                        session[f'project_count_{current_user.id}'] = project_count

                        if project_count == 2:
                            return jsonify({'redirect': url_for('student.home')})

                        flash(f'Project {project_count} submitted successfully', category='success')
                        return jsonify({'success': True})

                    except Exception as e:
                        db.session.rollback()
                        flash('Error submitting project. Please try again.', category='danger')
                        return jsonify({'error': str(e)}), 500
    else:
        flash("You are alone, form a group first", 'danger')
        return jsonify({'redirect': url_for("student.form_group")})

    return render_template('submit.html', title='Submit your project idea', form=form)


@student.route('/logout')
@login_required
@student_required
def logout():
    logout_user()
    return redirect(url_for('student.login'))







