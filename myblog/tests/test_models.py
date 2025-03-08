# tests/test_models.py
import os
import unittest
from datetime import datetime

from flask import Flask
from sqlalchemy.exc import IntegrityError

from config import config
from extensions import db
from models import User, Post


class ModelTestCase(unittest.TestCase):
    def setUp(self):
        # 创建测试应用实例
        self.app = Flask(__name__)
        self.app.config.from_object(config['test'])  # 需要先在config中添加test配置
        self.app_context = self.app.app_context()
        self.app_context.push()

        # 初始化数据库
        db.init_app(self.app)
        db.create_all()

        # 创建测试客户端
        self.client = self.app.test_client()

    def tearDown(self):
        # 清理数据库
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        """测试用户模型创建"""
        user = User(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        db.session.add(user)
        db.session.commit()

        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.password.startswith('password'))  # 实际中密码应该是哈希值

    def test_post_creation(self):
        """测试文章模型创建"""
        user = User(
            username='author1',
            email='author@example.com',
            password='password'
        )
        post = Post(
            title='Test Post',
            content='This is a test content',
            author=user
        )

        db.session.add_all([user, post])
        db.session.commit()

        self.assertEqual(post.title, 'Test Post')
        self.assertIsInstance(post.created_at, datetime)
        self.assertEqual(post.author, user)
        self.assertIn(post, user.posts)

    def test_username_uniqueness(self):
        """测试用户名唯一性约束"""
        user1 = User(username='duplicate', email='test1@example.com', password='pwd')
        user2 = User(username='duplicate', email='test2@example.com', password='pwd')

        db.session.add(user1)
        db.session.commit()

        with self.assertRaises(IntegrityError):
            db.session.add(user2)
            db.session.commit()

    def test_email_uniqueness(self):
        """测试邮箱唯一性约束"""
        user1 = User(username='user1', email='duplicate@example.com', password='pwd')
        user2 = User(username='user2', email='duplicate@example.com', password='pwd')

        db.session.add(user1)
        db.session.commit()

        with self.assertRaises(IntegrityError):
            db.session.add(user2)
            db.session.commit()
        db.session.rollback()

    def test_required_fields(self):
        """测试必填字段约束"""
        # 测试缺少用户名
        with self.assertRaises(IntegrityError):
            user = User(email='test@example.com', password='pwd')
            db.session.add(user)
            db.session.commit()
        db.session.rollback()

        # 测试缺少邮箱
        with self.assertRaises(IntegrityError):
            user = User(username='testuser', password='pwd')
            db.session.add(user)
            db.session.commit()
        db.session.rollback()

        # 测试缺少密码
        with self.assertRaises(IntegrityError):
            user = User(username='testuser', email='test@example.com')
            db.session.add(user)
            db.session.commit()
        db.session.rollback()

    def test_post_author_relationship(self):
        """测试文章与用户的关联关系"""
        # 创建用户和关联文章
        user = User(username='writer', email='writer@example.com', password='pwd')
        post1 = Post(title='Post 1', content='Content 1', author=user)
        post2 = Post(title='Post 2', content='Content 2', author=user)

        db.session.add_all([user, post1, post2])
        db.session.commit()

        # 验证关联关系
        self.assertEqual(len(user.posts), 2)
        self.assertEqual(post1.author_id, user.id)
        self.assertEqual(post2.author_id, user.id)
        self.assertEqual(user.posts[0].title, 'Post 1')

    def test_string_representation(self):
        """测试模型的字符串表示"""
        user = User(username='testuser', email='test@example.com', password='pwd')
        post = Post(title='Test Post', content='Content', author=user)

        self.assertEqual(str(user), f"<User 'testuser'>")
        self.assertEqual(str(post), f"<Post 'Test Post'>")


if __name__ == '__main__':
    unittest.main()