"""
    Copyright ⓒ 2024 Dcho, Inc. All Rights Reserved.
    Author : Dcho (tmdgns743@gmail.com)
    Description : User Model
"""

# System
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)

# Project
from core.models import BaseModel
from apps.users.manager import UserManager


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    """
    시스템 내 개발, 사용자를 나타내는 사용자 모델입니다.
    """

    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name="사용자 이메일 주소",
    )
    is_active = models.BooleanField(default=True, verbose_name="활성 사용자 여부")
    is_staff = models.BooleanField(default=False, verbose_name="어드민 여부")

    objects = UserManager()

    USERNAME_FIELD = "email"

    class Meta:
        app_label = "users"
        db_table = "users"

    def __str__(self) -> str:
        return self.email
