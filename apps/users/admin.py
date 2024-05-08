"""
    Copyright ⓒ 2024 Dcho, Inc. All Rights Reserved.
    Author : Dcho (tmdgns743@gmail.com)
    Description : User Admin
"""

# System
from django.contrib import admin

# Project
from apps.users.models import User

admin.site.register(User)
