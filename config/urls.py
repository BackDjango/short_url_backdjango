"""
    Copyright ⓒ 2024 Dcho, Inc. All Rights Reserved.
    Author : Dcho (tmdgns743@gmail.com)
    Description : Root Urls
"""

# System
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Project
from apps.short_url.views import ShortURLViewSet

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api", include(("apps.users.urls", "api-users"))),
    path("api", include(("apps.short_url.urls", "api-short-url"))),
    path(
        "<str:url>",
        ShortURLViewSet.as_view({"get": "get_redirect"}),
        name="get-redirect",
    ),
    path("<str:url>/+", ShortURLViewSet.as_view({"get": "get_visit_short_url"})),
]

# Swagger
from config.settings.swagger.setup import SwaggerSetup  # noqa

urlpatterns = SwaggerSetup.do_urls(urlpatterns=urlpatterns)

# Static/Media File Root (CSS, JavaScript, Images)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
