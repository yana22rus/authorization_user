import os
from datetime import datetime
import uuid
from flask import Blueprint, render_template, flash, request, redirect, url_for,abort
from project.forms import CreateNewsForm
from project.models import db, News

news_bp = Blueprint("news", __name__)

NEWS_PER_PAGE = 5

UPLOAD_FOLDER = os.path.join("img","uploads")

@news_bp.errorhandler(404)
def page_not_found(e):
    return "404", 404

@news_bp.route("/news", methods=["GET", "POST"])
@news_bp.route("/news/<int:page>", methods=["GET", "POST"])
def show_news(page=1):
    q = News.query.order_by(News.time.desc()).paginate(page, NEWS_PER_PAGE, error_out=False)

    if request.method == "POST":

        if request.form["submit"] == "Фильтр":
            filter = request.form["filter"]

            q = News.query.filter_by(title=filter).first()

            return render_template("filter_news.html", q=q)

        if request.form["submit"] == "Удалить":
            d = request.form.keys()
            id, *b = d

            News.query.filter_by(id=id).update({News.is_deleted: "1"})
            db.session.flush()
            db.session.commit()

            return redirect(url_for(".show_news"))

        if request.form["submit"] == "Восстановить":
            d = request.form.keys()
            id, *b = d

            News.query.filter_by(id=id).update({News.is_deleted: "0"})
            db.session.flush()
            db.session.commit()

            return redirect(url_for(".show_news"))

    return render_template("news.html", q=q)


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


@news_bp.route("/create_news", methods=["GET", "POST"])
def create_news():
    form = CreateNewsForm()

    if request.method == "POST" and form.validate_on_submit():

        file = request.files["file"]

        file_extensions = file.filename

        news = News.query.filter_by(title=request.form["title"]).first()

        if file_extensions.split(".")[-1].lower() not in ALLOWED_EXTENSIONS:

            flash("Не поддерживаемый тип файла", category='error')

            return render_template("create_news.html", form=form)


        elif news != None:

            flash("Дублирующий заголовок новости", category='error')

            return render_template("create_news.html",  form=form)

        else:

            file.filename = f'{uuid.uuid4()}.{file.filename.split(".")[-1].lower()}'

            file.save(os.path.join("static", UPLOAD_FOLDER, file.filename))

            create_news = News(login="admin",
                               time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), seo_title=request.form["seo_title"],
                               seo_description=request.form["seo_description"], title=request.form["title"],
                               subtitle=request.form["subtitle"], content_page=request.form["content_page"],
                               img=file.filename,is_deleted="0")

            db.session.add(create_news)
            db.session.flush()
            db.session.commit()

            flash("Успешно сохранено", category='success')

            q = News.query.filter_by(title=request.form["title"]).first()

            return redirect(f"/update_news/{q.id}")

    return render_template("create_news.html",  form=form)


@news_bp.route("/update_news/<int:news_id>", methods=["GET", "POST"])
def update_news(news_id):

    q = News.query.filter_by(id=news_id).first()

    if q == None or q.is_deleted == 1:

        abort(404)

    form = CreateNewsForm(seo_title=q.seo_title, seo_description=q.seo_description, title=q.title, subtitle=q.subtitle,
                          content_page=q.content_page)

    if request.method == "POST" and form.validate_on_submit():

        if request.form["submit"] == "Сохранить":

            q_title = News.query.filter_by(title=request.form["title"]).first()

            if q_title != None:

                flash("Дублирующий заголовок", category='error')

                return render_template("edit_news.html", q=q, form=form)

            file = request.files["file"]

            file_extensions = file.filename

            if file_extensions == "":

                News.query.filter_by(id=news_id).update({News.seo_title: request.form["seo_title"],
                                                         News.seo_description: request.form["seo_description"],
                                                         News.title: request.form["title"],
                                                         News.subtitle: request.form["subtitle"],
                                                         News.content_page: request.form["content_page"],
                                                         })
                db.session.flush()
                db.session.commit()

                flash("Успешно сохранено", category='success')

                return render_template("edit_news.html",  q=q, form=form)

            else:

                file.filename = f'{uuid.uuid4()}.{file.filename.split(".")[-1].lower()}'

                if file_extensions.split(".")[-1].lower() not in ALLOWED_EXTENSIONS:
                    flash("Не поддерживаемый тип файла", category='error')

                    return render_template("edit_news.html",  q=q, form=form)

                file.save(os.path.join("static", UPLOAD_FOLDER, file.filename))

            News.query.filter_by(id=news_id).update({News.seo_title: request.form["seo_title"],
                                                     News.seo_description: request.form["seo_description"],
                                                     News.title: request.form["title"],
                                                     News.subtitle: request.form["subtitle"],
                                                     News.content_page: request.form["content_page"],
                                                     News.img: file.filename
                                                     })

            db.session.flush()
            db.session.commit()

            flash("Успешно сохранено", category='success')

    if request.method == "POST":

        if request.form["submit"] == "Удалить":
            News.query.filter_by(id=news_id).update({News.is_deleted: "1"})
            db.session.flush()
            db.session.commit()

            return redirect(url_for(".show_news"))

    return render_template("edit_news.html",  q=q, form=form)


@news_bp.route("/main_news/<int:news_id>")
def main_news(news_id):
    news = News.query.filter_by(id=news_id).first()

    if news == None or news.is_deleted == 1:

        abort(404)

    return render_template("main_news.html", news=news)
