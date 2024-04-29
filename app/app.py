#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/28 9:51
# @Author  : Stepheng
# @Email   : 1142262478@qq.com
# @File    : config.py
# 功能描述  ：主应用入口
import sys
from flask import Flask
from .config import Config
from .routes import routes

sys.path.extend([r"/data/env/studyPoem-server/studypoem_server"])

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # 加载配置
    return app

if __name__ == '__main__':
    app = create_app()

    # 初始化数据库
    from .models import db
    db.init_app(app)

    # 注册路由
    app.register_blueprint(routes)

    app.run()