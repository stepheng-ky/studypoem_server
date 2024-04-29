#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/29 11:26
# @Author  : Stepheng
# @Email   : 1142262478@qq.com
# @File    : utils.py.py
# 功能描述  ：工具
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
def model_to_dict(model):
    """
    将Flask-SQLAlchemy模型对象转换为字典。
    """
    # 初始化一个空字典来存储属性
    if not model:
        return
    result = {}
    # 遍历模型对象的所有属性
    for column in model.__table__.columns:
        # 使用getattr来获取属性的值
        value = getattr(model, column.name)
        # 如果值是关系对象（比如另一个模型），则递归调用model_to_dict
        if isinstance(value, db.Model):
            value = model_to_dict(value)
        # 将属性名和值添加到字典中
        result[column.name] = value
    return result