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
db = SQLAlchemy(app)

from project.news.news import news_bp
app.register_blueprint(news_bp)

app.run(debug=True)