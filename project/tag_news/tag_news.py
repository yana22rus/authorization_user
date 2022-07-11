import os
from datetime import datetime
from flask import Blueprint, render_template, flash, request, redirect, url_for, abort
from project.forms import CreateTagNews
from project.models import db, Tag_news

tag_news_bp = Blueprint("tag_news", __name__)

NEWS_PER_PAGE = 5


@tag_news_bp.errorhandler(404)
def page_not_found(e):
    return "404", 404


@tag_news_bp.route("/tag_news", methods=["GET", "POST"])
@tag_news_bp.route("/tag_news/<int:page>", methods=["GET", "POST"])
def show_tag_news(page=1):
    q = Tag_news.query.order_by(Tag_news.time.desc()).paginate(page, NEWS_PER_PAGE, error_out=False)

    if request.method == "POST":

        if request.form["submit"] == "Удалить":
            d = request.form.keys()
            id, *b = d
            my_data = Tag_news.query.get(id)
            db.session.delete(my_data)
            db.session.commit()
            return redirect(url_for(".show_tag_news"))

    return render_template("tag_news.html", q=q)


@tag_news_bp.route("/create_tag_news", methods=["GET", "POST"])
def create_tag_news():
    form = CreateTagNews()

    if request.method == "POST" and form.validate_on_submit():

        q = Tag_news.query.filter_by(title=request.form["title"]).first()

        if q != None:

            flash("Дублирующий заголовок", category='error')

            return render_template("create_tag_news.html", form=form)


        else:

            create_tag_news = Tag_news(login="admin", time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                       title=request.form["title"])
            db.session.add(create_tag_news)
            db.session.flush()
            db.session.commit()

            flash("Успешно сохранено", category='success')

            q = Tag_news.query.filter_by(title=request.form["title"]).first()

            return redirect(url_for('.update_tag_news', tag_news_id=q.id))

    return render_template("create_tag_news.html", form=form)


@tag_news_bp.route("/update_tag_news/<int:tag_news_id>", methods=["GET", "POST"])
def update_tag_news(tag_news_id):
    q = Tag_news.query.filter_by(id=tag_news_id).first()

    form = CreateTagNews(title=q.title)

    if request.method == "POST" and form.validate_on_submit():

        if request.form["submit"] == "Сохранить":

            q_title = Tag_news.query.filter_by(title=request.form["title"]).first()

            if q_title != None:

                flash("Дублирующий заголовок", category='error')

                return render_template("edit_tag_news.html", q=q, form=form)

            Tag_news.query.filter_by(id=tag_news_id).update({Tag_news.title: request.form["title"]})
            db.session.flush()
            db.session.commit()
            flash("Успешно сохранено", category='success')

            return render_template("edit_tag_news.html", q=q, form=form)

    return render_template("edit_tag_news.html", q=q, form=form)
