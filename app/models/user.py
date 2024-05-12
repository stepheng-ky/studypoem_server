#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/29 11:28
# @Author  : Stepheng
# @Email   : 1142262478@qq.com
# @File    : user.py
# 功能描述  ：用户
from ..config import db


class Users(db.Model):
    user_id = db.Column(db.String(20), primary_key=True)
    user_name = db.Column(db.String(255))
    source = db.Column(db.String(20))
    avatarUrl = db.Column(db.String(255))


class UserPlans(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, primary_key=True)
    is_default = db.Column(db.Integer, default=0)
