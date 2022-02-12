from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin,login_required,login_user,logout_user
from werkzeug.security import generate_password_hash,check_password_hash


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


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@app.route("/")
def index():

    return render_template("index.html")

@app.route("/qwerty")
@login_required
def secret_page():

    return "secret_page"



@app.route("/login",methods=["GET","POST"])
def login():

    login = request.form.get("login")
    password = request.form.get("password")

    if login and password:

        user = Users.query.filter_by(login=login).first()

        if user and check_password_hash(user.password,password):

            login_user(user)

            return redirect("/qwerty")


    return render_template("page_login.html")


@app.route("/registration",methods=["GET","POST"])
def registration():

    if request.method == "POST":

        hash = generate_password_hash(request.form["password"])

        new_user = Users(

            login = request.form["login"],
            email = request.form["email"],
            password = hash,
            time_registration = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        )

        db.session.add(new_user)
        db.session.flush()
        db.session.commit()

        flash("Вы успешно зарегистрированы")

    return render_template("page_registration.html")


@app.route("/logout",methods=["GET","POST"])
def logout():

    logout_user()
    return redirect(url_for("index"))



if __name__ == "__main__":
    app.run(debug=True)