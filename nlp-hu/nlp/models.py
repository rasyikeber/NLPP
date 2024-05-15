
from flask_bcrypt import check_password_hash
from datetime import datetime, timezone
from nlp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
    dpt = db.Column(db.String(80))
    password = db.Column(db.String(80))
    is_student = db.Column(db.Boolean, default=False)
    is_dpthead = db.Column(db.Boolean, default=False)
    is_adviser = db.Column(db.Boolean, default=False)

    def __init__(self, name, email,  dpt, password, is_student=False, is_dpthead=True,is_adviser=False):
        self.name = name
        self.email = email
        self.dpt =dpt
        self.password = password
        self.is_student = is_student
        self.is_dpthead = is_dpthead
        self.is_adviser =is_adviser
      
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def update_dpthead_status(self, is_dpthead):
        self.is_dpthead = is_dpthead
        db.session.commit()

class Student(User):
    studid = db.Column(db.Integer, unique=True)
    year = db.Column(db.Integer)
    is_grouped = db.Column(db.Boolean, default=False)
    group_id = db.Column(db.String(100))

    def __init__(self, name, email,  dpt, password, studid, year, is_grouped=False, group_id=None):
        super().__init__(name, email, dpt, password, is_student=True,is_dpthead=False)
        self.studid = studid
        self.year = year
        self.is_grouped = is_grouped
        self.group_id = group_id

    def update_isgrpd_status_and_gr_id(self, is_grouped, group_id):
        self.is_grouped = is_grouped
        self.group_id = group_id
        db.session.commit()
 
class Adviser(User):
    special_in = db.Column(db.String(80))

    def __init__(self, name, email,dpt,password, special_in):
        super().__init__(name, email,dpt, password, is_adviser=True,is_dpthead=False)
        self.special_in = special_in
      


# Define the OldProject table
class Oldproject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(500))
    year = db.Column(db.Integer)

    def __init__(self, title, description, year):
        self.title = title
        self.description = description
        self.year = year

    def delete(self):
        db.session.delete(self)
        db.session.commit()


# Define the NewProject table
class Newproject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True)
    description = db.Column(db.String(255), unique=True)
    pdpt = db.Column(db.String(50))
    group_id = db.Column(db.String(100)) # check
    adviser_name = db.Column(db.String(100),default =None)
    is_approved = db.Column(db.Boolean, default=False)
    year = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))
    def __init__(self, title, description, group_id, adviser_name, year, pdpt, date, is_approved=False):
        self.title = title
        self.description = description
        self.pdpt = pdpt
        self.group_id = group_id
        self.adviser_name=adviser_name
        self.is_approved= is_approved
        self.year = year
        self.date = date

    def save(self):
        db.session.add(self)
        db.session.commit()
    def update_project_status(self, is_approved):
        self.is_approved=is_approved
        db.session.commit()
    def update_project_advisor(self, adviser_name):
        self.adviser_name = adviser_name
        db.session.commit()

    def update(self, title=None, description=None, group_id=None, year=None, pdpt=None):
        if title:
            self.title = title
        if description:
            self.description = description
        if group_id:
            self.group_id = group_id
        if year:
            self.year = year
        if pdpt:
            self.pdpt = pdpt
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()