from project import db

# class Users(db.Model,UserMixin):
#
#     id = db.Column(db.Integer, primary_key=True)
#     login =db.Column(db.String, nullable=True)
#     email = db.Column(db.String, nullable=True)
#     password = db.Column(db.String, nullable=True)
#     time_registration = db.Column(db.String, nullable=True)
#
#     def is_authenticated(self):
#         return True
#
#     def is_active(self):
#         return True
#
#     def is_anonymous(self):
#         return False




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
    tag_news = db.Column(db.String, nullable=False)


class Quiz(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, nullable=True)
    time = db.Column(db.String, nullable=True)
    seo_title = db.Column(db.String, nullable=True)
    seo_description = db.Column(db.String, nullable=True)
    title = db.Column(db.String, nullable=True)
    subtitle = db.Column(db.String, nullable=True)
    question_answers = db.Column(db.String, nullable=True)


class Tag_news(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, nullable=True)
    time = db.Column(db.String, nullable=True)
    title = db.Column(db.String, nullable=True)




class User_auth_log(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String, nullable=True)
    login = db.Column(db.String, nullable=True)


class Survey(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title_survey = db.Column(db.String, nullable=True)

    survey = db.Column(db.String, nullable=True)

    login = db.Column(db.String, nullable=True)