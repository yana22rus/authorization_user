from getpass import getuser
import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

UPLOAD_FOLDER = os.path.join("img", "uploads")
app = Flask(__name__)
app.secret_key = "key"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:////home/{getuser()}/main.sqlite'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1042 * 1042

footer = [{"name":"Пользователи","url":"/users"},{"name":"Роли","url":"/role"},
            {"name":"Права доступа","url":"/permission"},
            {"name":"Логи авторизации","url":"/logs_authorization"}]

side_bar = [{"name":"Новости","url":"/news"},{"name":"Документы","url":"/document"},{"name":"Опрос","url":"/survey"},
                 {"name":"Викторина","url":"/quiz"},
                 {"name":"Структура","url":"/structure"},{"name":"Теги новостей","url":"/tag_news"},
                 {"name":"Теги документов","url":"/tag_document"},{"name":"Фоторепортажи","url":"/photo_report"},
                 {"name":"Видеорепортажи","url":"/video_report"},{"name":"Список опечаток","url":"/typo_repor"},
                 ]

app.jinja_env.globals.update(footer=footer)
app.jinja_env.globals.update(side_bar=side_bar)
db = SQLAlchemy(app)

from project.news.news import news_bp
from project.tag_news.tag_news import tag_news_bp
from project.quiz.quiz import quiz_bp
app.register_blueprint(news_bp)
app.register_blueprint(tag_news_bp)
app.register_blueprint(quiz_bp)

app.run(debug=True)