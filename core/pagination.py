"""
    Copyright ⓒ 2024 Dcho, Inc. All Rights Reserved.
    Author : Dcho (tmdgns743@gmail.com)
    Description : Custom Pagination
"""

# System
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

# Project
from core.constants import SYSTEM_CODE


class CustomPagination(PageNumberPagination):
    """
    Custom Pagination
    페이지 네이션은 이것으로 관리합니다.
    """

    page_size = 10

    def get_paginated_response(self, **kwargs):

        status = kwargs.get("status", 200)
        code = kwargs.get("code", SYSTEM_CODE.SUCCESS)
        msg = kwargs.get("msg", code[1])
        data = kwargs.get("data", None)

        payload = {
            "links": {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
            },
            "count": self.page.paginator.count,
            "data": data,
            "status_code": status,
            "msg": msg,
            "code": code[0],
        }

        return Response(data=payload, status=status)
