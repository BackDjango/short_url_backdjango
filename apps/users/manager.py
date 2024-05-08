"""
    Copyright ⓒ 2024 Dcho, Inc. All Rights Reserved.
    Author : Dcho (tmdgns743@gmail.com)
    Description : User Manager
"""

# System
from django.db import models
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    사용자 모델 관리자로, 사용자 생성 및 관리를 처리합니다.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        이메일, 비밀번호 및 추가 필드를 사용하여 새로운 사용자를 생성하고 변환합니다.

        이메일이 제공되지 않을 경우 ValueError를 발생시킵니다.
        """

        if not email:
            raise ValueError("이메일 주소를 필수로 가져야 합니다.")

        email = self.normalize_email(email=email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password=None):
        """
        Create and return a new superuser.
        """

        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user
