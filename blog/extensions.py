from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_mail import Mail

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
ckeditor = CKEditor()
mail = Mail()