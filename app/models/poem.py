#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/29 11:27
# @Author  : Stepheng
# @Email   : 1142262478@qq.com
# @File    : poem.py
# 功能描述  ：诗词
from ..config import db

class Poems(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    yiwen = db.Column(db.Text)
    zhailu = db.Column(db.Text)
    author_short = db.Column(db.String(100), nullable=False)