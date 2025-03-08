from flask import Blueprint, render_template
from ..models import User, Post
from flask_login import login_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')

@admin_bp.route('/manage_users')
@login_required
def manage_users():
    users = User.query.all()
    return render_template('admin/manage_users.html', users=users)

@admin_bp.route('/manage_posts')
@login_required
def manage_posts():
    posts = Post.query.all()
    return render_template('admin/manage_posts.html', posts=posts)