from flask import Blueprint
from flask import render_template, request, current_app, redirect, url_for

from blog.models import Category, Post, Comment
from blog.forms import CommentForm
from blog.extensions import db

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
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config["BLOG_POST_PER_PAGE"]
    pagination = Comment.query.with_parent(post).order_by(Comment.timestamp.asc()).paginate(page, per_page)
    comments = pagination.items
    form = CommentForm()
    from_admin = False
    reviewed = False
    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        site = form.site.data
        body = form.body.data
        comment = Comment(author=author, email=email, site=site, body=body, from_admin=from_admin, post=post, reviewed=reviewed)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for("blog.show_post", post_id=post_id))
    return render_template('blog/post.html', post=post, pagination=pagination, comments=comments, form=form)


@blog_bp.route("/comment/<int:comment_id>", methods=["GET", "POST"])
def reply_comment(comment_id):
    return render_template()