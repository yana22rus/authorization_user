from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from main import db
from main import app
import os

UPLOAD_FOLDER = os.path.join("img","uploads")

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


class Users(db.Model,UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    login =db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    password = db.Column(db.String, nullable=True)
    time_registration = db.Column(db.String, nullable=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False


login_manager = LoginManager(app)


class News(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, nullable=True)
    time = db.Column(db.String, nullable=True)
    seo_title = db.Column(db.String, nullable=True)
    seo_description = db.Column(db.String, nullable=True)
    title = db.Column(db.String, nullable=True)
    subtitle = db.Column(db.String, nullable=True)
    content_page = db.Column(db.String, nullable=True)
    short_link = db.Column(db.String, nullable=False)
    img = db.Column(db.String, nullable=False)
    is_deleted = db.Column(db.Integer, nullable=False)



class User_auth_log(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String, nullable=True)
    login = db.Column(db.String, nullable=True)


class Survey(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title_survey = db.Column(db.String, nullable=True)

    survey = db.Column(db.String, nullable=True)

    login = db.Column(db.String, nullable=True)