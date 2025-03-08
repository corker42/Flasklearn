from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

# 初始化数据库
db = SQLAlchemy()
# 初始化 CSRF 保护
csrf = CSRFProtect()