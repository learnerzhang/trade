#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-08-16 11:47
# @Author  : zhangzhen
# @Site    : 
# @File    : page_utils.py
# @Software: PyCharm

class Pagination(object):
    """
    自定义分页
    """
    def __init__(self, current_page, total_count, page_size):
        self.current_page = current_page
        self.page_size = page_size
        self.total_count = total_count

    @property
    def page_count(self):
        nums = int(self.total_count / self.page_size)
        return nums if self.total_count % self.page_size == 0 else nums + 1

    @property
    def is_first_page(self):
        return self.current_page == 1 or self.total_count == 0

    @property
    def is_last_page(self):
        return self.current_page >= self.page_count or self.total_count == 0

    @property
    def has_next_page(self):
        return self.current_page < self.page_count

    @property
    def get_next_page(self):
        return self.current_page + 1 if self.current_page < self.page_count else self.page_count

    @property
    def has_prev_page(self):
        return self.current_page > 1

    def get_prev_page(self):
        return self.current_page - 1 if self.current_page > 1 else 1

    @property
    def offset(self):
        return (self.current_page - 1) * self.page_size if self.current_page > 0 else 0

    @property
    def end(self):
        return self.current_page * self.page_size