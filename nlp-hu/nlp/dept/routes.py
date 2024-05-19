from flask import render_template, Blueprint, flash, redirect, url_for,request,session
from nlp.dept.forms import  AddProject, DeptRegistrationForm, DeptLoginForm
from  nlp.models import User, Student, Adviser,Newproject
from flask_login import login_user, current_user, logout_user, login_required
from nlp import db, bcrypt
from functools import wraps
from collections import defaultdict

def department_head_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the current user is authenticated and is a department head
        if not current_user.is_authenticated or not current_user.is_dpthead:
            # Redirect the user to the login page or display an error message
            flash('You are not authorized to access this page.', 'danger')
            return redirect(url_for('dept.dept_login'))
        return f(*args, **kwargs)
    return decorated_function


dept= Blueprint('dept',__name__)

@dept.route('/dept-signup',methods=['GET','POST'])
def dept_signup():
  if current_user.is_authenticated:
    return redirect(url_for('dept.dept_home'))
  form =DeptRegistrationForm()
  if form.validate_on_submit():
    hashed_password =bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    dept = User(name=form.name.data, email=form.email.data, dpt=form.dpt_head_of.data, password=hashed_password)
    db.session.add(dept)
    db.session.commit()
    flash(f'your account has been created!', 'success')
    return redirect(url_for('dept.dept_login'))
  return render_template('dept-signup.html', title= "department sign up", form=form)

@dept.route('/dept-login', methods=['GET', 'POST'])
def dept_login():
  form = DeptLoginForm()
  if current_user.is_authenticated and current_user.is_dpthead:
    return redirect(url_for('dept.dept_home'))
  else:
    if form.validate_on_submit():
      head = User.query.filter_by(email=form.email.data).first()
      print(head)
      if head and bcrypt.check_password_hash(head.password, form.password.data):
        login_user(head, remember=form.remember.data)
        redirect(url_for('dept.dept_home'))
        #  next_page = request.args.get('next')
        #  return redirect(next_page) if next_page else redirect(url_for('dept.dept_home'))
      else:
        flash('Login Unsuccessful. Please check student ID and password.', 'danger')
  return render_template('dept-login.html', title='dept Login', form=form)


@dept.route('/dept-home', methods=['GET', 'POST'])
@login_required
@department_head_required
def dept_home():
   
   allProjects=Newproject.query.filter_by(pdpt=current_user.dpt).all()
   projects = [project for project in allProjects if project.is_approved == True]
   adv= Adviser.query.all()
   advisors = [advisor for advisor in adv if advisor.is_adviser == True]
   return render_template('assign.html', title='assign advisor to students',
                          user=current_user,
                          projects=projects,
                          advisors=advisors,
                          )

@dept.route('/dashboard-projectidea', methods=['GET', 'POST'])
@login_required
@department_head_required
def dashboard_project():
    grouped_data = []
    if current_user.is_dpthead:
      #print(current_user.is_dpthead)
      dept = current_user.dpt
      projects = Newproject.query.filter_by(pdpt=dept).filter_by(is_approved=None).all()
      print("wtf", len(projects))
      if projects:
         
        students = Student.query.filter_by(dpt=dept).all()
        # print(students, projects)
        if not projects and not students:
          print("No projects found for department:", dept)
          #  Grouping students by group_id
        else:
         students_by_group = defaultdict(list)
         for student in students:
             students_by_group[student.group_id].append(student)
            
            
        # Grouping projects by group_id

         projects_by_group = defaultdict(list)
         for project in projects:
             projects_by_group[project.group_id].append(project)
            
        # Combining projects and students for each group_id


         for group_id, group_projects in projects_by_group.items():
            group_students = students_by_group[group_id]
            grouped_data.append({
                'group_id': group_id,
                'projects': group_projects,
                'students': group_students
            })
      else:
         print("no project unapproved is here")
         if not len(grouped_data) >0:
          print("empty list 0",grouped_data)
            

    return render_template('dashboard.html', title='all Project Idea', user =current_user, grouped_data=grouped_data)


@dept.route('/approved-projectidea', methods=['GET', 'POST'])
@login_required
@department_head_required
def approved_project():
    grouped_data = []
    if current_user.is_dpthead:
      #print(current_user.is_dpthead)
      dept = current_user.dpt
      projects = Newproject.query.filter_by(pdpt=dept).filter_by(is_approved=True).all()
      print(len(projects))

      students = Student.query.filter_by(dpt=dept).all()
      # print(students, projects)
      if not projects and not students:
         print("No projects found for department:", dept)
        #  Grouping students by group_id
      else:
         students_by_group = defaultdict(list)
         for student in students:
             students_by_group[student.group_id].append(student)
            
            
        # Grouping projects by group_id

         projects_by_group = defaultdict(list)
         for project in projects:
             projects_by_group[project.group_id].append(project)
            
        # Combining projects and students for each group_id


         for group_id, group_projects in projects_by_group.items():
            group_students = students_by_group[group_id]
            grouped_data.append({
                'group_id': group_id,
                'projects': group_projects,
                'students': group_students
            })
          

    return render_template('approved.html', title='all Project Idea', user =current_user, grouped_data=grouped_data)






@dept.route('/add-projectidea', methods=['GET', 'POST'])
@login_required
@department_head_required
def add_project_idea():
  form =AddProject()
  
  currentUser = Student.query.filter_by(id=current_user.id).first()
  grp_id = currentUser.group_id
  
  if form.validate_on_submit():
    try:
      project = Newproject( title=form.title.data,
                            description=form.description.data,
                            group_id=grp_id, 
                            pdpt=form.dept.data,
                            year=form.year.data, 
                            date=form.submission_date.data)
      db.session.add(project)  
      db.session.commit()
      # Increment the project count
      project_count += 1
      # Update the session variable with the new project count specific to the user
      session[f'project_count_{current_user.id}'] = project_count
      flash(f'Project {project_count} submitted successfully', category='success')
      # Check if the student has submitted two projects and redirect if true
      if project_count == 2:
        flash('You have successfully submitted two projects', category='success')
        return redirect(url_for('dept.dept_home'))
    except Exception as e:
        flash('Error submitting project. Please try again.', category='error')
        print(f"Error: {str(e)}")

  return render_template('add-project.html', title='add project', form=form)




@dept.route('/assign-advisor', methods=['GET', 'POST'])
@login_required
@department_head_required
def assign_advisor():
  if request.method == 'POST':
    print(request.form)
    # Retrieve the selected advisor's name from the form
    # get group id here   ()
    groupID=request.form.get('groupID')
    advisor_name = request.form.get('advisor_name')
    num_of_advisor=Newproject.query.filter_by(adviser_name=advisor_name).count()
    if num_of_advisor >4:
        flash(f"mr. {advisor_name} assigned for three Group with three d/t project",'danger')
        return redirect(url_for('dept.dept_home'))
    else:
        project=Newproject.query.filter_by(group_id=groupID).first()
        if project.is_approved:
          project.update_project_advisor(advisor_name)
          print("assigned to a project ",project)
          flash("advisor assigned successfully",'success')
        else:
          print("update was not successfull")
  return redirect(url_for('dept.dept_home'))


@dept.route('/reject-projectidea', methods=['GET', 'POST'])
@login_required
@department_head_required
def reject_project():
    if request.method == 'POST':
        data = request.json
        group_id = data.get('groupId')
        # Retrieve the project with the given group_id
        project = Newproject.query.filter_by(group_id=group_id).first()
        print(project.id)
        if project:
            # Delete the project
            # db.session.delete(project)
            # db.session.commit()
            print(f"the project deleted with group ID:  {project.group_id}")
            # return "Project with groupID {} rejected successfully.".format(group_id)
            return redirect(url_for('dashboard_project'))
        else:
            print("no project found")
            return "No project found with groupID {}.".format(group_id)
            
    else:
        return "This endpoint only accepts POST requests."
   

@dept.route('/approve-projectidea', methods=['GET', 'POST'])
def approve_dashboard():
  if request.method == 'POST':
        data = request.json
        projectId_str = data.get('projectId')
        projectId = int(projectId_str)
        # Retrieve the     project with the given projectId
        project_byId = Newproject.query.get(projectId)
        if project_byId is not None:
            # Retrieve all projects with the same group_id as the project_byId
            projects = Newproject.query.filter_by(group_id=project_byId.group_id).all()
            #update project status
            for project in projects:
               project.update_project_status(True)
            projects_to_delete = [project for project in projects if project.id != projectId]
            # Delete the remaining projects
            for project in projects_to_delete:
                print("project not selected by dept head", project)
                db.session.delete(project)
                db.session.commit()
                flash("project approved successfully, you can now assign advisor to this project",'success')
            return redirect(url_for('dept.dashboard_project'))     
  return "Received group_id from flask backend project id: " + str(projectId)


@dept.route('/dept-logout')
@login_required
@department_head_required
def dept_logout():
    logout_user()
    return redirect(url_for('dept.dept_login'))
