from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired,Email,Length

class LoginForm(FlaskForm):

    login = StringField("Логин",validators=[Length(min=4,max=100,message="Логин должен быть от 4 до 100 символов")],name="login")
    email = StringField("Email",validators=[Email("Некорректный email")])
    password = PasswordField("Пароль",validators=[DataRequired(),Length(min=4,max=100,message="Пароль должен быть от 4 до 100 символов")])
    submit = SubmitField("Сохранить")