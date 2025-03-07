import os
import sys

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

WINDOWS = sys.platform.startswith('win')
if WINDOWS: # Windows-specific configuration
    prefix = 'sqlite:///'
else: # Linux/Mac-specific configuration
    prefix = 'sqlite:////'
app = Flask(__name__) # Create Flask app instance

# app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:abc123456@localhost:3306/flaskdb' # 请根据您的 MySQL 环境修改
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的监控

# Initialize SQLAlchemy instance to the Flask app instance
db = SQLAlchemy(app) # Initialize SQLAlchemy


# Define your models here
class User(db.Model): # 表名将会是 user（自动生成，小写处理）
    __tablename__ = 'user' # 表名可以自定义
    id = db.Column(db.Integer, primary_key=True) # 主键
    name = db.Column(db.String(20)) # 名字

class Movie(db.Model): # 表名将会是 movie
    __tablename__ ='movie' # 表名可以自定义
    id = db.Column(db.Integer, primary_key=True) # 主键
    title = db.Column(db.String(60)) # 电影名称
    year = db.Column(db.String(4)) # 电影年份

if __name__ == '__main__':
    db.drop_all() # 删除所有表
    db.create_all() # 创建所有表

    user = User(name='John Doe') # 创建 User 实例
    m1 = Movie(title='Inception', year='2010') # 创建 Movie 实例
    m2 = Movie(title='The Matrix', year='1999') # 创建 Movie 实例
    m3 = Movie(title='Eternal Sunshine of the Spotless Mind', year='2004') # 创建 Movie 实例
    db.session.add(user) # 加入到会话
    db.session.add_all([m1, m2, m3]) # 加入到会话
    db.session.commit() # 提交会话




