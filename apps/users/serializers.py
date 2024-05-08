"""
    Copyright ⓒ 2024 Dcho, Inc. All Rights Reserved.
    Author : Dcho (tmdgns743@gmail.com)
    Description : User Serializers
"""

# System
from django.db import IntegrityError
from rest_framework import serializers

# Project
from apps.users.models import User
from core.exception import raise_exception
from core.constants import SYSTEM_CODE
from core.jwt import CustomJWTAuthentication


class SignUpSerializer(serializers.Serializer):
    """
    회원가입 시리얼라이저
    """

    email = serializers.EmailField(max_length=255, required=True, write_only=True, label="[Input]이메일")
    password = serializers.CharField(max_length=128, required=True, write_only=True, label="[Input]패스워드")

    access_token = serializers.CharField(read_only=True, label="[Output]access_token")
    refresh_token = serializers.CharField(read_only=True, label="[Output]refresh_token")

    def validate_email(self, data):
        """
        Email 중복 검증
        """
        if User.objects.filter(email=data).exists():
            raise_exception(code=SYSTEM_CODE.EMAIL_ALREADY)
        return data

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]

        try:
            user = User.objects.create_user(email=email, password=password)
        except IntegrityError:
            raise_exception(code=SYSTEM_CODE.USER_CREATE_ERROR)

        return CustomJWTAuthentication.create_token(user=user)


class SignInSerializer(serializers.Serializer):
    """
    로그인 시리얼라이저
    """

    email = serializers.EmailField(max_length=255, required=True, write_only=True, label="[Input]이메일")
    password = serializers.CharField(max_length=128, required=True, write_only=True, label="[Input]패스워드")

    access_token = serializers.CharField(read_only=True, label="[Output]access_token")
    refresh_token = serializers.CharField(read_only=True, label="[Output]refresh_token")

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = User.objects.filter(email=email).first()

        # 존재 하지 않는 유저
        if not user:
            raise_exception(code=SYSTEM_CODE.USER_NOT_FOUND)

        # 비밀번호 불일치
        if not user.check_password(raw_password=password):
            raise_exception(code=SYSTEM_CODE.USER_INVALID_PW)

        # 비활성화 유저
        if not user.is_active:
            raise_exception(code=SYSTEM_CODE.USER_NOT_ACTIVE)

        return CustomJWTAuthentication.create_token(user=user)


class TokenRefreshSerializer(serializers.Serializer):
    """
    토큰 재발급 시리얼 라이저
    """

    token = serializers.CharField(max_length=255, required=True, write_only=True, label="[Input]refresh_token")

    access_token = serializers.CharField(read_only=True, label="[Output]access_token")
    refresh_token = serializers.CharField(read_only=True, label="[Output]refresh_token")

    def validate(self, data):
        refresh_token = data.get("token")

        user = CustomJWTAuthentication.validate_token(refresh_token)

        return CustomJWTAuthentication.create_token(user=user)
