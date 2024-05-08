"""
    Copyright ⓒ 2024 Dcho, Inc. All Rights Reserved.
    Author : Dcho (tmdgns743@gmail.com)
    Description : User Urls
"""

# System
from django.urls import path, include

# Project
from apps.users.views import AuthViewSet

auth_urls = [
    path("/signup", AuthViewSet.as_view({"post": "sign_up"}), name="sign-up"),
    path("/signin", AuthViewSet.as_view({"post": "sign_in"}), name="sign-in"),
    path(
        "/token/refresh",
        AuthViewSet.as_view({"post": "token_refresh"}),
        name="token-refresh",
    ),
]

urlpatterns = [
    path("/auth", include(auth_urls)),
]
