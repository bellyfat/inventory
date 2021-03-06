# -*- coding: utf-8 -*-
#
# inventory/common/api/pagination.py
#
"""
Global pagination
"""
__docformat__ = "restructuredtext en"

from rest_framework.pagination import PageNumberPagination


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 200
