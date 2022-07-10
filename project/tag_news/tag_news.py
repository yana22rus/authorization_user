import os
from datetime import datetime
import uuid
from flask import Blueprint, render_template, flash, request, redirect, url_for,abort
from project.forms import CreateTagNews
from project.models import db, Tag_news

tag_news_bp = Blueprint("tag_news", __name__)

NEWS_PER_PAGE = 5

@tag_news_bp.errorhandler(404)
def page_not_found(e):
    return "404", 404

@tag_news_bp.route("/tag_news", methods=["GET", "POST"])
@tag_news_bp.route("/tag_news/<int:page>", methods=["GET", "POST"])
def tag_news(page=1):

    q = Tag_news.query.order_by(Tag_news.time.desc()).paginate(page, NEWS_PER_PAGE, error_out=False)

    return render_template("tag_news.html",q=q)


@tag_news_bp.route("/create_tag_news", methods=["GET", "POST"])
def create_tag_news():

    form = CreateTagNews()

    if request.method == "POST" and form.validate_on_submit():
        create_tag_news = Tag_news(login="admin",time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),title=request.form["title"])
        db.session.add(create_tag_news)
        db.session.flush()
        db.session.commit()

    return render_template("create_tag_news.html",form=form)


@tag_news_bp.route("/update_tag_news/<int:tag_news_id>", methods=["GET", "POST"])
def update_tag_news(tag_news_id):

    q = Tag_news.query.filter_by(id=tag_news_id).first()

    form = CreateTagNews(title=q.title)

    return render_template("edit_tag_news.html",q=q,form=form)