from datetime import datetime
import os
from getpass import getuser
from flask import Flask,render_template,request,redirect,flash,url_for,make_response
from data_base import *
from flask_login import login_required,login_user,logout_user,current_user
from werkzeug.security import generate_password_hash,check_password_hash
from forms import LoginForm

UPLOAD_FOLDER = os.path.join("img","uploads")

app = Flask(__name__)

app.secret_key = "key"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:////home/{getuser()}/main.sqlite'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1042 * 1042
db = SQLAlchemy(app)




side_bar = [{"name":"Пользователи","url":"/users"},{"name":"Роли","url":"/role"},{"name":"Права доступа","url":"/permission"},{"name":"Логи авторизации","url":"/logs_authorization"}]

side_bar_main = [{"name":"Новости","url":"/news"},{"name":"Документы","url":"/document"},{"name":"Опрос","url":"/survey"},
                 {"name":"Викторина","url":"/quiz"},
                 {"name":"Структура","url":"/structure"},{"name":"Теги новостей","url":"/tag_news"},
                 {"name":"Теги документов","url":"/tag_document"},{"name":"Фоторепортажи","url":"/photo_report"},
                 {"name":"Видеорепортажи","url":"/video_report"},{"name":"Список опечаток","url":"/typo_repor"},
                 ]


@app.route("/")
@app.route("/index")
def index():

    return render_template("index.html")

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

        q = Users.query.filter_by(login=form.login.data).first()

        return render_template("edit_user.html", side_bar=side_bar, q=q)


    return render_template("page_registration.html",side_bar=side_bar,form=form)

@app.route("/update_user/<int:user_id>",methods=["GET","POST"])
@login_required
def update_user(user_id):

    q = Users.query.filter_by(id=user_id).first()

    if request.method == "POST":

        Users.query.filter_by(id=user_id).update({Users.login:request.form["login"],Users.email: request.form["email"]})



        db.session.flush()
        db.session.commit()

        flash("Успешно сохранено", category='success')


    return render_template("edit_user.html",side_bar=side_bar,q=q)





@app.route("/admin")
@login_required
def admin():

    return render_template("admin.html",side_bar=side_bar)

@app.route("/logs_authorization")
@login_required
def logs_authorization():

    join_table = db.session.query(User_auth_log,Users).join(Users,Users.login == User_auth_log.login).all()

    return render_template("logs_authorization.html", side_bar=side_bar,join_table=join_table)


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

        return render_template("users.html",side_bar=side_bar,items=Users.query.all())

    return render_template("users.html",side_bar=side_bar,items=Users.query.all())



@app.route("/main")
@login_required
def main():
    return render_template("main.html",side_bar_main=side_bar_main)



@app.route("/main_news/<int:news_id>")
def main_news(news_id):

    news = News.query.filter_by(id=news_id).first()

    return render_template("main_news.html",news=news)

@app.route("/survey",methods=["GET","POST"])
@login_required
def survey():

    res = db.session.query(Users, Survey).join(Users, Users.login == Survey.login).all()

    if request.method == "POST":


        d = request.form.keys()
        id,*b= d

        my_data = Survey.query.get(id)
        db.session.delete(my_data)
        db.session.commit()

        return redirect(url_for("survey"))

    return render_template("survey.html",side_bar_main=side_bar_main,res=res)


@app.route("/create_survey",methods=["GET","POST"])
@login_required
def create_survey():

    if request.method == "POST":

        lst = []

        for x in request.form.listvalues():

            if x == [request.form["title_survey"]]:

                continue

            lst.append("".join(x))

        lst = ":".join(lst)

        create_survey = Survey(title_survey=request.form["title_survey"],survey=lst,login=current_user.login)

        db.session.add(create_survey)
        db.session.flush()
        db.session.commit()

        flash("Успешно сохранено")

        return redirect(url_for("survey"))


    return render_template("create_survey.html",side_bar_main=side_bar_main)



@app.route("/main_survey/<int:survey_id>",methods=["GET","POST"])
def main_survey(survey_id):

    q = Survey.query.filter_by(id=survey_id).first()

    lst = q.survey.split(":")

    if request.method == "POST":

        vote = request.form["field"]

        with open(f"results_survey{survey_id}.txt","a") as f:

            f.writelines(vote+"\n")

        return redirect(url_for('results_survey',survey_id=survey_id))

    return render_template("main_survey.html",lst=lst,q=q)

@app.route("/results_survey/<int:survey_id>")
def results_survey(survey_id):

    votes = {}

    q = Survey.query.filter_by(id=survey_id).first()

    lst = q.survey.split(":")

    for x in lst:

        votes[x] = 0

    with open(f"results_survey{survey_id}.txt") as f:

        for line in f:

            vote = line.strip("\n")

            votes[vote] += 1

    return render_template("results.html",votes=votes,q=q)

@app.route("/quiz")
@login_required
def quiz():

    return render_template("quiz.html",side_bar_main=side_bar_main)


@app.route("/create_quiz",methods=["GET","POST"])
@login_required
def create_quiz():

    # TODO

    if request.method == "POST":

        lst = []

        for x in request.form.listvalues():

            lst.append("".join(x))


    return render_template("create_quiz.html",side_bar_main=side_bar_main)


@app.route("/role")
@login_required
def role():

    return "TODO"

@app.route("/permission")
@login_required
def permission():

    return "TODO"


if __name__ == "__main__":
    app.run(debug=True,port=5000)