from flask import Blueprint, render_template, request, redirect, url_for
from ..models import User, Post
from ..forms import LoginForm
from ..extensions import db
from flask_login import login_user, logout_user, login_required, current_user

user_bp = Blueprint('user', __name__)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('user/login.html', form=form)

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@user_bp.route('/profile')
@login_required
def profile():
    return render_template('user/profile.html')

@user_bp.route('/posts')
@login_required
def posts():
    user = User.query.get(current_user.id)
    user_posts = user.posts.all()
    return render_template('user/posts.html', posts=user_posts)