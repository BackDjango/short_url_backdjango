"""
    Copyright ⓒ 2024 Dcho, Inc. All Rights Reserved.
    Author : Dcho (tmdgns743@gmail.com)
    Description : Short URL Admin
"""

# System
from django.contrib import admin

# Project
from apps.short_url.models import ShortURL

admin.site.register(ShortURL)
