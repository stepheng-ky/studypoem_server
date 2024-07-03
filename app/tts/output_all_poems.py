#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/2 21:41
# @Author  : Stepheng
# @Email   : 1142262478@qq.com
# @File    : output_all_poems.py
# 功能描述  ：导出所有poems到 poems_file

from ..services import _get_all_poems,_get_one_random_poem
def _out_poems():
    poems = _get_all_poems()
    for poem in poems:
        id = poem.get('id')
        title = poem.get('title')
        author = poem.get('author')
        content = poem.get('content')
        # file_name = f'./poems_file/{id}.txt'
        file_name = f'app/tts/poems_file/{id}.txt'
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(title + '\n')
            file.write(author + '\n')
            file.write(content)
    return f'完成all.'
