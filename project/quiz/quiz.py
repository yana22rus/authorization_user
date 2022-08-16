import json
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, abort
from project.forms import CreateQuizForm
from project.models import db, Quiz

quiz_bp = Blueprint("quiz", __name__)


@quiz_bp.route("/quiz", methods=["GET", "POST"])
@quiz_bp.route("/quiz/<int:page>", methods=["GET", "POST"])
def show_quiz(page=1):
    pass


@quiz_bp.route("/create_quiz", methods=["GET", "POST"])
def create_quiz():
    form = CreateQuizForm()

    if request.method == "POST":


        lst = []

        for x in request.form.listvalues():
            lst.append("".join(x))


        lst = lst[4:][:-1:]

        d = dict(zip(lst[::1], lst[::2]))

        print(d)

        create_quiz = Quiz(login="admin",
                           time=datetime.now().strtime("%Y-%m-%d %H:%M:%S"), seo_title=request.form["seo_title"],
                           seo_description=request.form["seo_description"], title=request.form["title"],
                           subtitle=request.form["subtitle"], question_answers=json.dumps(d))
        db.session.add(create_quiz)
        db.session.flush()
        db.session.commit()

    return render_template("create_quiz.html", form=form)


@quiz_bp.route("/main_quiz/<int:quiz_id>")
def main_quiz(quiz_id):
    quiz = Quiz.query.filter_by(id=quiz_id).first()

    lst_tag_data = json.loads(quiz.question_answers)

    for k in lst_tag_data:
        print(k)

    if quiz == None:
        abort(404)

    return render_template("main_quiz.html")
