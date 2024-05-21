"""
    Copyright ⓒ 2024 Dcho, Inc. All Rights Reserved.
    Author : Dcho (tmdgns743@gmail.com)
    Description : Short URL Config
"""

from django.apps import AppConfig


class ShortUrlConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.short_url"
