#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/5/8 17:27
# @Author  : Stepheng
# @Email   : 1142262478@qq.com
# @File    : footprints.py
# 功能描述  ：足迹
from ..config import db


class Footprints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    province = db.Column(db.String(255), nullable=False)
    light_up_time = db.Column(db.String(255), nullable=False)
    light_up_img = db.Column(db.String(255))
