from flask import Blueprint
from flask import render_template, request, current_app

from blog.models import Category, Post

blog_bp = Blueprint("blog", __name__)


@blog_bp.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    return render_template("blog/index.html", posts=pagination.items, pagination=pagination)


@blog_bp.route("/category/<int:category_id>", methods=["GET"])
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    return render_template("blog/category.html", category=category)


@blog_bp.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('blog/post.html', post=post)