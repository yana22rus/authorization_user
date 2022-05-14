from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired,Email,Length

class LoginForm(FlaskForm):

    login = StringField("Логин",validators=[Length(min=4,max=100,message="Логин должен быть от 4 до 100 символов")],name="login")
    email = StringField("Email",validators=[Email("Некорректный email")])
    password = PasswordField("Пароль",validators=[DataRequired(),Length(min=4,max=100,message="Пароль должен быть от 4 до 100 символов")])
    submit = SubmitField("Сохранить")


class CreateNewsForm(FlaskForm):

    title = StringField("Заголовок",validators=[Length(min=4,max=255,message="Заголовок должен быть от 4 до 255 символов")],name="title")

    subtitle = StringField("Подзаголовок",validators=[Length(max=255,message="Подзаголовок должен быть до 255 символов")],name="subtitle")

    content = StringField("Содержимое",validators=[Length(max=255,message="Содержимое должен быть до 255 символов")],name="content")

