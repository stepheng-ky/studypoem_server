#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/29 11:28
# @Author  : Stepheng
# @Email   : 1142262478@qq.com
# @File    : plan.py
# 功能描述  ：学习计划
from ..config import db


class Plans(db.Model):
    plan_id = db.Column(db.Integer, primary_key=True)
    plan_name = db.Column(db.String(255))
    is_public = db.Column(db.Integer, default=1)
    start_date = db.Column(db.Date)


class PlanDetails(db.Model):
    plan_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(255), primary_key=True)
    poem_sort = db.Column(db.Integer, nullable=False)
    is_learned = db.Column(db.Integer)
