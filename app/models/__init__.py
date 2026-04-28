from flask_sqlalchemy import SQLAlchemy

# 初始化 SQLAlchemy 實例
db = SQLAlchemy()

# 匯入所有的 Models 確保 Flask 能註冊它們
from .category import Category
from .recipe import Recipe
