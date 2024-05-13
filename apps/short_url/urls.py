"""
    Copyright ⓒ 2024 Dcho, Inc. All Rights Reserved.
    Author : Dcho (tmdgns743@gmail.com)
    Description : Short URL Url
"""

# System
from django.urls import path, include

# Project
from apps.short_url.views import ShortURLViewSet

short_url_urls = [
    path("", ShortURLViewSet.as_view({"post": "post_short_url"}), name="post-short-url"),
    path(
        "/<str:url>",
        ShortURLViewSet.as_view({"delete": "delete_short_url"}),
        name="delete-short-url",
    ),
]


urlpatterns = [
    path("/shorturl", include(short_url_urls)),
]
