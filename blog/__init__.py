import os
import click
from flask import Flask

from blog.blueprints import admin, auth, blog
from blog.extensions import bootstrap, moment, db, ckeditor, mail
from blog.models import User, Category, Post, Comment, Link
from blog.setting import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", "development")

    app = Flask("blog")
    app. config.from_object(config[config_name])

    register_blueprints(app)
    register_extensions(app)
    register_template_context(app)
    register_shell_content(app)
    register_commands(app)

    return app


def register_blueprints(app):
    app.register_blueprint(admin.admin_bp)
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(blog.blog_bp)


def register_extensions(app):
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)


def register_shell_content(app):
    @app.shell_context_processor
    def make_shell_content():
        return dict(db=db, User=User,  Category=Category, Post=Post, Comment=Comment)


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        user = User.query.first()
        categories = Category.query.order_by(Category.name).all()
        return dict(
            user=user, categories=categories,
        )


def register_commands(app):
    @app.cli.command()
    @click.option("--drop", is_flag=True, help="Create after drop")
    def init_db(drop):
        """Initialize the database."""
        if drop:
            click.confirm("This is operation will delete the database, do you want to continue? ", abort=True)
            db.drop_all()
            click.echo("Drop tables.")
        db.create_all()
        click.echo("Initialized database.")

    @app.cli.command()
    @click.option("--username", prompt=True, help="The username used to login.")
    @click.option("--password", prompt=True, help="The password used to login.")
    def init_user(username, password):
        """Buliding Blog, just for you"""
        click.echo("Initializing the database...")
        db.create_all()

        user = User.query.first()
        if user is not None:
            click.echo("The User already exists, updating")
            user.username = username
            user.set_password(password)
        else:
            click.echo("Creating the temporary user account")
            user = User(
                username=username,
                blog_title="Blog",
                blog_sub_title="Sub title",
                name="User",
                about="Something for you"
            )
            user.set_password(password)
            db.session.add(user)

        category = Category.query.first()
        if category is not None:
            click.echo("Creating the default category...")
            category = Category(name="default category")
            db.session.add(category)

        db.session.commit()
        click.echo("Done")
