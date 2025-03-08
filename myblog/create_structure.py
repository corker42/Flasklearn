import os

# 获取当前脚本所在的目录，也就是 myblog 目录
main_dir = os.path.dirname(os.path.abspath(__file__))

# 定义文件和文件夹结构
file_structure = [
    ("app.py", ""),
    ("config.py", ""),
    ("extensions.py", ""),
    ("models.py", ""),
    ("forms.py", ""),
    ("templates", [
        ("base.html", ""),
        ("index.html", ""),
        ("user", [
            ("login.html", ""),
            ("profile.html", ""),
            ("posts.html", "")
        ]),
        ("admin", [
            ("dashboard.html", ""),
            ("manage_users.html", ""),
            ("manage_posts.html", "")
        ])
    ]),
    ("static", [
        ("css", []),
        ("js", []),
        ("images", [])
    ]),
    ("blueprints", [
        ("user_bp.py", ""),
        ("admin_bp.py", "")
    ]),
    ("tests", [
        ("__init__.py", ""),
        ("test_app.py", ""),
        ("test_models.py", ""),
        ("test_forms.py", "")
    ])
]

def create_structure(base_dir, structure):
    for item in structure:
        if isinstance(item, tuple):
            name, content = item
            path = os.path.join(base_dir, name)
            if isinstance(content, list):
                # 如果是文件夹，创建文件夹并递归调用
                if not os.path.exists(path):
                    os.makedirs(path)
                create_structure(path, content)
            else:
                # 如果是文件，创建文件并写入内容
                if not os.path.exists(path):
                    with open(path, 'w') as f:
                        f.write(content)

# 创建目录结构和文件
create_structure(main_dir, file_structure)

print(f"目录结构和文件已成功创建在 {main_dir} 中。")