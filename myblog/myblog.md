# MyBlog

## 文件结构

```bash
Myblog/
│
├── app.py                   # 主应用入口文件
├── config.py                # 配置文件
├── extensions.py            # 扩展初始化文件（如数据库等）
├── models.py                # 数据库模型定义
├── forms.py                 # 表单类定义（用于用户登录、注册等表单）
├── templates/               # 模板文件夹
│   ├── base.html            # 基础模板
│   ├── index.html           # 首页模板
│   ├── user/
│   │   ├── login.html       # 用户登录页面模板
│   │   ├── profile.html     # 用户个人信息页面模板
│   │   └── posts.html       # 用户发布的文章页面模板
│   └── admin/
│       ├── dashboard.html   # 后台管理员仪表盘模板
│       ├── manage_users.html # 管理用户页面模板
│       └── manage_posts.html# 管理文章页面模板
├── static/                  # 静态文件文件夹（CSS、JavaScript、图片等）
│   ├── css/
│   ├── js/
│   └── images/
├── blueprints/              # 蓝图文件夹，用于模块化组织代码
│   ├── user_bp.py           # 用户相关蓝图
│   └── admin_bp.py          # 管理员相关蓝图
└── tests/                   # 测试文件夹
    ├── __init__.py          # 使tests成为一个Python包
    ├── test_app.py          # 测试应用基本功能的文件
    ├── test_models.py       # 测试数据库模型的文件
    └── test_forms.py        # 测试表单的文件
```

## 开发步骤

1. **基础骨架搭建（优先验证环境）**
   - 先创建 `config.py` 配置基础项（SECRET_KEY/SQLALCHEMY_DATABASE_URI）
   - 编写 `extensions.py` 初始化数据库、登录管理器等扩展
   - 创建最简版 `app.py` 验证Flask应用能否启动
2. **核心数据模型（先于功能开发）**
   - 在 `models.py` 中定义 `User` 和 `Post` 模型（需包含基础字段）
   - 通过Flask-SQLAlchemy的命令行工具生成初始数据库
3. **功能验证（先完成最小闭环）**
   - 在 `app.py` 中临时添加一个测试路由（如首页显示"Hello World"）
   - 添加 `/login` 临时路由测试表单基础交互
4. **模块化拆解（保持代码整洁）**
   - 将临时路由迁移到 `blueprints/user_bp.py`
   - 创建 `forms.py` 实现登录/注册表单类
5. **模板体系搭建（最后完善界面）**
   - 先做 `templates/base.html` 基础模板
   - 逐步填充 `index.html` 和 `login.html`