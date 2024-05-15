from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from nlp.config import Config



db=SQLAlchemy()
bcrypt =Bcrypt()
login_manager =LoginManager()
login_manager.login_view = 'student.login'
login_manager.login_message_category = 'info'



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from nlp.student.routes import student
    from nlp.advisor.routes import advisors
    from nlp.dept.routes import dept
    from nlp.errors.handlers import errors

    app.register_blueprint(student)
    app.register_blueprint(advisors)
    app.register_blueprint(dept)
    app.register_blueprint(errors)
    return app

# database craetion
# from nlp  import app, db
# with app.app_context():
#  db.create_all()