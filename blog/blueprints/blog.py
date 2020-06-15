from flask import Blueprint
from flask import render_template

from blog.models import Category, Post

blog_bp = Blueprint("blog", __name__)


@blog_bp.route("/")
def index():
    return render_template("base.html")


@blog_bp.route("/main")
def main():
    return render_template("base.html")


@blog_bp.route("/category/<int:category_id>", methods=["GET"])
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    return render_template("blog/category.html", category=category)


@blog_bp.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('blog/post.html', post=post)


@blog_bp.route("/posts", methods=["GET"])
def show_posts():
    posts = Post.query.order_by(Post.id).all()
    return render_template('blog/posts.html', posts=posts)