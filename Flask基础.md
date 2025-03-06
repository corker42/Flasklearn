

## Flask基本概念

### 一、Flask 核心概念图谱

text

```text
[客户端请求] → [WSGI Server] → [Flask App] → 
    ↓
[Routing] → [View Function] → 
    ↓
[Request Context] → [Jinja2 Templates] → 
    ↓
[Response] → [WSGI Server] → [客户端]
```

------

### 二、核心术语详解

#### 1. WSGI (Web Server Gateway Interface)

- Python 标准 Web 应用接口
- **示例角色**：Gunicorn 是 WSGI 服务器，Flask 是 WSGI 应用

#### 2. Application Object (应用对象)

python

```python
app = Flask(__name__)  # 核心容器对象
```

- 包含配置、路由、扩展等所有应用状态

#### 3. View Function (视图函数)

python

```python
@app.route('/')
def home():
    return render_template('index.html')
```

- 处理请求并返回响应（直接返回字符串或调用模板）

#### 4. Request Context (请求上下文)

- `request`：包含客户端请求数据（表单、Cookies 等）
- `session`：用户会话存储
- **生命周期**：每个请求独立存在

#### 5. Blueprint (蓝图)

python

```python
admin_bp = Blueprint('admin', __name__)
@admin_bp.route('/dashboard')
def dashboard():
    return "Admin Panel"
```

- 模块化组织大型应用的组件

------

### 三、Flask 框架完整处理流程

#### 请求生命周期流程图

text

```text
1. 客户端发起请求
2. WSGI 服务器接收请求
3. 创建应用上下文和请求上下文
4. URL 调度器匹配路由
5. 执行视图函数（可能访问数据库）
6. 生成响应对象
7. 销毁请求上下文
8. 返回响应到客户端
```

#### 分步解析：

1. **上下文创建**：

   python

   ```python
   # 伪代码演示上下文栈
   ctx = app.request_context(environ)
   ctx.push()  # 激活上下文
   ```

2. **路由匹配**：

   python

   ```python
   # 路由映射表示例
   Map([<Rule '/about' (HEAD, GET) -> about>,
        <Rule '/user/<username>' (HEAD, GET) -> user>])
   ```

3. **视图处理**：

   python

   ```python
   # 典型的请求处理流程
   @app.route('/submit', methods=['POST'])
   def submit():
       data = request.form['content']
       # 数据库操作...
       return redirect(url_for('result'))
   ```

4. **响应生成**：

   python

   ```python
   # 可返回多种类型
   return "Text"                    # 字符串
   return render_template(...)      # 模板
   return jsonify({'data': ...})    # JSON
   return redirect(...)             # 重定向
   ```

------

### 四、核心架构组件

#### 1. 组件关系图

text

```text
        [Extensions]
           ↑
[App] → [Config] → [Routes] → [Views]
           ↓               ↖ [Templates]
[Contexts] → [Request/Response]
```

#### 2. 关键对象关系

- **应用上下文**：管理应用级数据 (如数据库连接)
- **请求上下文**：存储请求级数据 (如表单数据)
- **配置系统**：`app.config` 字典存储配置参数

------

### 五、开发流程示例

#### 典型文件结构

text

```text
/myapp
   ├── app.py          # 应用入口
   ├── config.py       # 配置文件
   ├── templates/      # Jinja2 模板
   ├── static/         # 静态文件
   └── blueprints/     # 蓝图模块
```

#### 基础代码模板

python

```python
from flask import Flask
app = Flask(__name__)

# 加载配置
app.config.from_pyfile('config.py')

# 注册蓝图
from blueprints.admin import admin_bp
app.register_blueprint(admin_bp)

# 核心路由
@app.route('/')
def index():
    return 'Home Page'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

------

### 六、关键记忆表

|        概念        |        作用场景        |      典型方法/属性      |
| :----------------: | :--------------------: | :---------------------: |
|   `current_app`    | 访问应用上下文中的对象 |        代理对象         |
|    `url_for()`     |      反向生成 URL      | endpoint 作为第一个参数 |
|      `g` 对象      |  请求周期内的全局存储  |     跨函数共享数据      |
|  `before_request`  |     预处理每个请求     |     装饰器注册函数      |
| `teardown_request` |   请求结束后清理资源   |  即使发生异常也会执行   |

------

### 七、高级流程解析

**数据库集成流程**：

text

```text
[请求进入] → 打开数据库连接 → 处理业务逻辑 → 
    ↓
提交或回滚事务 → 关闭连接 → [返回响应]
```

**模板渲染流程**：

text

```text
调用 render_template() → Jinja2 加载模板 → 
    ↓
解析变量和逻辑 → 生成 HTML → 返回响应
```

## Flask 快速入门

## 🌟 第一阶段：基础核心概念

### 1. 快速入门

python

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, Flask World!'

if __name__ == '__main__':
    app.run(debug=True)
```

💡 关键点：

- `Flask(__name__)` 初始化应用实例
- `@app.route()` 装饰器定义路由
- `debug=True` 启用调试模式（仅用于开发）

### 2. 动态路由

python

```python
@app.route('/user/<username>')
def show_user(username):
    return f'User: {username}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Post #{post_id}'
```

📌 路径转换器：

- `string`: 默认（不含斜线）
- `int`: 整型
- `float`: 浮点数
- `path`: 类似字符串但包含斜线

### 3. 请求处理基础

python

```python
from flask import request

@app.route('/search')
def search():
    keyword = request.args.get('q', '')
    return f'Searching for: {keyword}'
```

## Flask 路由的变量规则和端点

### 一、变量规则详解

#### 1. 基础语法

python

```python
@app.route('/user/<username>')
def show_user(username):
    return f'Username: {username}'
```

- `<variable>` 捕获 URL 片段作为字符串（默认转换器）
- 变量会作为参数传递给视图函数

#### 2. 类型转换器

python

```python
@app.route('/post/<int:post_id>')        # 整型
@app.route('/price/<float:price>')       # 浮点数
@app.route('/path/<path:subpath>')       # 包含斜线的路径
@app.route('/uuid/<uuid:uuid_val>')      # UUID 格式
```

**示例测试：**

python

```python
# 访问 /post/abc → 404 Not Found（类型不匹配）
# 访问 /post/123 → 正常显示 Post ID: 123
```

#### 3. 自定义正则匹配（高级）

python

```python
from werkzeug.routing import BaseConverter

class RegexConverter(BaseConverter):
    def __init__(self, url_map, regex):
        super().__init__(url_map)
        self.regex = regex

app.url_map.converters['re'] = RegexConverter

@app.route('/phone/<re(r'\d{11}'):phone>')
def show_phone(phone):
    return f'Valid phone: {phone}'
```

📌 这个路由只会匹配11位数字的URL，如：`/phone/13812345678`

------

### 二、端点（endpoint）详解

#### 1. 基本概念

- **端点**是路由的唯一标识符
- 默认端点是视图函数名
- 用于 `url_for()` 反向生成 URL

#### 2. 显式指定端点

python

```python
@app.route('/about', endpoint='about_page')
def about():
    return "About Page"

# 在模板或代码中调用
url_for('about_page')  # → 生成 /about
```

#### 3. 端点冲突示例

python

```python
# 错误示例：两个路由使用相同 endpoint
@app.route('/admin', endpoint='special')
def admin_dashboard():
    return "Admin"

@app.route('/user', endpoint='special')  # 会报错 ValueError
def user_profile():
    return "User"
```

#### 4. 视图函数复用（不同端点）

python

```python
@app.route('/blog/', endpoint='blog_list')
@app.route('/blog/<int:page>', endpoint='blog_paged')
def show_blog(page=1):
    return f'Blog Page {page}'

# 使用区别：
url_for('blog_list')   # → /blog/
url_for('blog_paged', page=2)  # → /blog/2
```

------

### 三、综合应用示例

#### 用户资料系统

python

```python
@app.route('/user/<username>', endpoint='user_profile')
def show_user_profile(username):
    return f'''
        <h1>{username}'s Profile</h1>
        <p>View posts: <a href="{url_for('user_posts', username=username)}">Posts</a></p>
    '''

@app.route('/user/<username>/posts')
def user_posts(username):
    return f'{username}\'s posts page'

# 测试访问：
# /user/alice → 显示资料页，包含指向 /user/alice/posts 的链接
```

------

### 关键记忆点 🔑

|     概念     |                        说明                        |
| :----------: | :------------------------------------------------: |
|   变量规则   |      使用 `<类型:变量名>` 格式捕获动态URL片段      |
|  默认转换器  |    string（默认）、int、float、path、uuid、any     |
|   端点作用   | 1. URL反向生成 2. 路由唯一标识 3. 蓝图命名空间管理 |
|   最佳实践   |    显式设置 endpoint 可避免大型项目中的命名冲突    |
| url_for 技巧 |   使用端点名称 + 参数生成 URL，而不是硬编码路径    |

## Jinja2 模板引擎的常用语法

### 一、基础语法结构

#### 1. 变量输出

jinja2

```jinja2
<p>用户名: {{ user.name }}</p>
<p>商品价格: {{ product.price | round(2) }}</p>
```

**特性**：

- 自动 HTML 转义（安全防护）
- 支持 `|` 管道过滤器
- 可访问对象属性/字典键值

#### 2. 控制结构

jinja2

```jinja2
{# 条件判断 #}
{% if score >= 90 %}
    <div class="excellent">优秀</div>
{% elif score >= 60 %}
    <div class="pass">及格</div>
{% else %}
    <div class="fail">不及格</div>
{% endif %}

{# 循环结构 #}
<ul>
{% for item in items %}
    <li>{{ loop.index }}. {{ item.name }}</li>
{% endfor %}
</ul>
```

**循环变量**：

- `loop.index`: 当前迭代次数（从1开始）
- `loop.revindex`: 反向迭代次数
- `loop.first`: 是否第一次迭代
- `loop.last`: 是否最后一次迭代

------

### 二、高级功能

#### 1. 模板继承

**基础模板 (base.html)**：

jinja2

```jinja2
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
    {% block css %}{% endblock %}
</head>
<body>
    <div class="content">
        {% block content %}{% endblock %}
    </div>
    {% block scripts %}{% endblock %}
</body>
</html>
```

**子模板 (child.html)**：

jinja2

```jinja2
{% extends "base.html" %}

{% block title %}用户中心 - 我的网站{% endblock %}

{% block css %}
    <link rel="stylesheet" href="/static/user.css">
{% endblock %}

{% block content %}
    <h1>欢迎, {{ username }}!</h1>
    {% include "partials/nav.html" %}
{% endblock %}
```

#### 2. 宏 (Macros)

**定义宏**：

jinja2

```jinja2
{% macro render_comment(comment) %}
    <div class="comment">
        <h3>{{ comment.author }}</h3>
        <p>{{ comment.text }}</p>
        <small>{{ comment.date | date_format }}</small>
    </div>
{% endmacro %}
```

**使用宏**：

jinja2

```jinja2
{{ render_comment(top_comment) }}

{% for comment in comments %}
    {{ render_comment(comment) }}
{% endfor %}
```

------

### 三、实用过滤器

#### 常用内置过滤器

jinja2

```jinja2
{{ "HELLO" | lower }}           → "hello"
{{ 3.1415926 | round(2) }}      → 3.14
{{ "<script>" | safe }}         → 禁用自动转义（慎用！）
{{ text | truncate(50) }}       → 截断至50字符
{{ items | join(", ") }}        → 列表转字符串
{{ var | default("N/A") }}      → 默认值
```

#### 自定义过滤器 (app.py)

python

```python
@app.template_filter('date_format')
def format_datetime(value, format="%Y-%m-%d %H:%M"):
    return value.strftime(format)
```

**模板中使用**：

jinja2

```jinja2
{{ post.created_at | date_format("%m/%d/%Y") }}
```

------

### 四、特殊语法技巧

#### 1. 注释

jinja2

```jinja2
{# 这是单行注释 #}

{#
  多行
  注释
#}
```

#### 2. 空白控制

jinja2

```jinja2
{% for item in list -%}  {# 移除前面的换行 #}
    {{ item }}
{%- endfor %}            {# 移除后面的换行 #}
```

#### 3. 赋值操作

jinja2

```jinja2
{% set navigation = [('home', 'Home'), ('about', 'About')] %}
{% set username = user.name | upper %}
```

------

### 五、安全实践

#### 1. 自动转义机制

- 默认开启 HTML 转义

- 禁用转义方法：

  jinja2

  ```jinja2
  {{ html_content | safe }}
  ```

  python

  ```python
  # Python 端标记安全内容
  from flask import Markup
  return render_template('page.html', content=Markup(safe_html))
  ```

#### 2. 防止 XSS

jinja2

```jinja2
{# 危险示例（不要这样做！） #}
{{ user_input }}               → 自动转义
{{ user_input | safe }}        → 潜在 XSS 漏洞
```

------

### 六、综合应用示例

#### 商品列表页

jinja2

```jinja2
{% extends "layout.html" %}

{% block title %}商品列表{% endblock %}

{% block content %}
  <div class="product-grid">
    {% for product in products %}
      <div class="product-card">
        <h3>{{ product.name | truncate(30) }}</h3>
        <p class="price">{{ product.price | format_currency }}</p>
        {% if product.stock > 0 %}
          <button>加入购物车</button>
        {% else %}
          <p class="stockout">缺货中</p>
        {% endif %}
      </div>
    {% else %}
      <p class="empty">暂无商品</p>
    {% endfor %}
  </div>
{% endblock %}
```

------

### 速查表

|      语法       |      用途      |            示例            |
| :-------------: | :------------: | :------------------------: |
|   `{{ ... }}`   |    变量输出    |     `{{ user.name }}`      |
| `{% if ... %}`  |    条件判断    |    `{% if age >= 18 %}`    |
| `{% for ... %}` |    循环结构    |  `{% for item in list %}`  |
|  `{% macro %}`  | 定义可复用组件 |   `{% macro render() %}`   |
| `{% include %}` |   嵌入子模板   | `{% include 'nav.html' %}` |
|        `        |    filter`     |         应用过滤器         |