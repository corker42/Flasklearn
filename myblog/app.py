from flask import Flask, render_template
from config import config
from extensions import db, csrf
from blueprints.user_bp import user_bp
from blueprints.admin_bp import admin_bp
from flask_login import LoginManager
from models import User

# 初始化 Flask 应用
app = Flask(__name__)
# 加载配置
app.config.from_object(config['default'])

# 初始化扩展
db.init_app(app)
csrf.init_app(app)

# 初始化 Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 注册蓝图
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(admin_bp, url_prefix='/admin')

# 首页路由
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)