#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/29 11:28
# @Author  : Stepheng
# @Email   : 1142262478@qq.com
# @File    : category.py
# 功能描述  ： 诗词类别

from ..config import db

class Categories(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255), nullable=False)


class CategoryPoem(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    second_level_category = db.Column(db.String(255))
    id = db.Column(db.String(255), primary_key=True)