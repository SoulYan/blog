from extensions import db
from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

from blog.models import Category


class LoginForm(FlaskForm):
    username = StringField("账号", validators=[DataRequired(), Length(1, 20)])
    password = PasswordField("密码", validators=[DataRequired(), Length(8, 128)])
    remember = BooleanField("记住")
    submit = SubmitField("登陆")


class PostForm(FlaskForm):
    title = StringField("标题", validators=[DataRequired(), Length(1, 60)])
    body = CKEditorField("内容", validators=[DataRequired()])
    category = SelectField("类别", coerce=int, default=1)
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name) for category in Category.query.order_by(Category.name).all()]
