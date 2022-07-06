import os
from datetime import datetime
import uuid
from flask import Blueprint,render_template,flash,request,redirect
from project.forms import CreateNewsForm
from project.models import db,News


news_bp = Blueprint("news",__name__)


UPLOAD_FOLDER = os.path.join("img","uploads")


ALLOWED_EXTENSIONS = {"png","jpg","jpeg"}
@news_bp.route("/create_news",methods=["GET","POST"])
def create_news():

    form = CreateNewsForm()

    if request.method == "POST" and form.validate_on_submit():

        file = request.files["file"]

        file_extensions = file.filename

        news = News.query.filter_by(title=request.form["title"]).first()

        if file_extensions.split(".")[-1].lower() not in ALLOWED_EXTENSIONS:

            flash("Не поддерживаемый тип файла", category='error')

            return render_template("create_news.html", side_bar_main=side_bar_main,form=form)


        elif news != None:

            flash("Дублирующий заголовок новости", category='error')

            return render_template("create_news.html", side_bar_main=side_bar_main,form=form)

        else:

            file.filename = f'{uuid.uuid4()}.{file.filename.split(".")[-1].lower()}'

            file.save(os.path.join("static",UPLOAD_FOLDER,file.filename))

            create_news = News(login="admin",
                               time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),seo_title=request.form["seo_title"],
                               seo_description=request.form["seo_description"],title=request.form["title"],
                               subtitle=request.form["subtitle"],content_page=request.form["content_page"],img=file.filename,is_deleted=0)

            db.session.add(create_news)
            db.session.flush()
            db.session.commit()

            flash("Успешно сохранено",category='success')

            q = News.query.filter_by(title=request.form["title"]).first()

            return redirect(f"/update_news/{q.id}")

    return render_template("create_news.html",form=form)