"""
    Copyright ⓒ 2024 Dcho, Inc. All Rights Reserved.
    Author : Dcho (tmdgns743@gmail.com)
    Description : Swagger Setup
"""

# System
from django.urls import path
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


class SwaggerSetup:
    """
    Swagger 셋팅
    """

    def do_urls(urlpatterns):
        # Swagger URL 설정
        if settings.DEBUG:
            urlpatterns += [
                path("schema/", SpectacularAPIView.as_view(), name="schema"),
                path(
                    "docs/",
                    SpectacularSwaggerView.as_view(url_name="schema"),
                    name="swagger-ui",
                ),
            ]
        return urlpatterns
