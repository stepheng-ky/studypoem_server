#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/29 11:31
# @Author  : Stepheng
# @Email   : 1142262478@qq.com
# @File    : plan_service.py
# 功能描述  ：计划服务
from app.models import Plans, PlanDetails
from app.services import _get_poem_by_id
from app.utils import model_to_dict


def _get_plan_by_id(plan_id):
    """
    根据plan_id获取plan信息
    """
    plan = model_to_dict(Plans.query.get(plan_id))
    return plan


def _get_plan_details_by_id(plan_id):
    """
    根据plan_id获取plan详细信息
    """
    plans = [model_to_dict(plan) for plan in PlanDetails.query.filter_by(plan_id=plan_id).order_by(PlanDetails.poem_sort.asc()) ]
    for plan in plans:
        plan['learn_time'] = plan['learn_time'].strftime("%Y-%m-%d %H:%M:%S") if plan['learn_time'] else None # 时间格式化
        poem = _get_poem_by_id(plan['id'])
        plan['title'] = poem['title']
        plan['zhailu'] = poem['zhailu']
    return plans
