from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin,login_required,login_user,logout_user
from werkzeug.security import generate_password_hash,check_password_hash
from forms import LoginForm

app = Flask(__name__)
app.secret_key = "key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/qwe/users.sql'
db = SQLAlchemy(app)

login_manager = LoginManager(app)

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

class User_auth_log(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String, nullable=True)
    login = db.Column(db.String, nullable=True)






@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@app.route("/")
@app.route("/index")
@login_required
def index():

    return render_template("sidebars.html")

@app.route("/admin_panel")
@login_required
def admin_panel():

    return render_template("base.html")



@app.route("/login",methods=["GET","POST"])
def login():

    login = request.form.get("login")
    password = request.form.get("password")

    if login and password:

        user = Users.query.filter_by(login=login).first()

        if user and check_password_hash(user.password,password):

            login_user(user)

            user_auth_log = User_auth_log(login=login,time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            db.session.add(user_auth_log)
            db.session.flush()
            db.session.commit()

            return redirect(url_for("admin_panel"))


    return render_template("page_login.html")


@app.route("/registration",methods=["GET","POST"])
@login_required
def registration():

    form = LoginForm()

    if form.validate_on_submit():

        hash = generate_password_hash(form.password.data)

        new_user = Users(

        login = form.login.data,
        email = form.email.data,
        password = hash,
        time_registration = datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


        db.session.add(new_user)
        db.session.flush()
        db.session.commit()

        flash("Вы успешно зарегистрированы")


        return redirect(url_for("registration"))


    return render_template("page_registration.html",side_bar=side_bar,form=form)

@app.route("/update_user/<int:user_id>",methods=["GET","POST"])
@login_required
def update_user(user_id):

    q = Users.query.filter_by(id=user_id).first()

    if request.method == "POST":

        pass


    return render_template("edit_user.html",side_bar=side_bar,q=q)



side_bar = [{"name":"Пользователи","url":"users"},{"name":"Роли","url":"role"},{"name":"Права доступа","url":"permission"},{"name":"Логи авторизации","url":"logs_authorization"}]

@app.route("/admin")
@login_required
def admin():

    return render_template("admin.html",side_bar=side_bar)

@app.route("/logs_authorization")
@login_required
def logs_authorization():

    return render_template("logs_authorization.html", side_bar=side_bar, items=User_auth_log.query.all())


@app.route("/logout",methods=["GET","POST"])
@login_required
def logout():

    logout_user()
    return redirect(url_for("login"))

@app.route("/users",methods=["GET","POST"])
@login_required
def users():


    if request.method == "POST":


        d = request.form.keys()
        id,*b= d

        my_data = Users.query.get(id)
        db.session.delete(my_data)
        db.session.commit()

        return render_template("sidebars_admin.html",side_bar=side_bar,items=Users.query.all())

    return render_template("sidebars_admin.html",side_bar=side_bar,items=Users.query.all())

side_bar_main = [{"name":"Новости","url":"news"},{"name":"Документы","url":"document"},{"name":"Опрос","url":"survey"},
                 {"name":"Структура","url":"structure"},{"name":"Теги новостей","url":"tag_news"},
                 {"name":"Теги документов","url":"tag_news"},{"name":"Фоторепортажи","url":"photo_report"},
                 {"name":"Видеорепортажи","url":"video_report"},{"name":"Список опечаток","url":"typo_repor"},
                 ]

@app.route("/main")
@login_required
def main():
    return render_template("main.html",side_bar_main=side_bar_main)

@app.route("/news")
@login_required
def news():

    return render_template("news.html",side_bar_main=side_bar_main)

@app.route("/create_news")
@login_required
def create_news():

    return render_template("create_news.html",side_bar_main=side_bar_main)

@app.route("/aaa")
@login_required
def aaa():

    return render_template("sidebars_admin.html")


if __name__ == "__main__":
    app.run(debug=True)