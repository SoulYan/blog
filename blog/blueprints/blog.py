from flask import Blueprint
from flask import render_template

blog_bp = Blueprint("blog", __name__)


@blog_bp.route("/")
def index():
    return render_template("base.html")

@blog_bp.route("/main")
def main():
    return render_template("base.html")