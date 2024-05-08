"""
    Copyright ⓒ 2024 Dcho, Inc. All Rights Reserved.
    Author : Dcho (tmdgns743@gmail.com)
    Description : Custom Renderer
"""

# System
from rest_framework.renderers import JSONRenderer

# Project
from core.constants import SYSTEM_CODE


class CustomRenderer(JSONRenderer):
    """
    CustomRenderer를 통해 전역 반환값을 설정
    """

    def render(self, data, accepted_media_type=None, renderer_context=None, **kwargs):
        response_data = renderer_context.get("response")
        status = kwargs.get("status", 200)
        code = kwargs.get("code", SYSTEM_CODE.SUCCESS)
        msg = kwargs.get("msg", code[1])

        response = {
            "data": data,
            "status_code": status,
            "msg": msg,
            "code": code[0],
        }
        # response = {
        #     "data": data,
        #     "status_code": response_data.status_code,
        #     "msg": response_data.status_text,
        # }

        return super(CustomRenderer, self).render(response, accepted_media_type, renderer_context)
