"""
    Copyright ⓒ 2024 Dcho, Inc. All Rights Reserved.
    Author : Dcho (tmdgns743@gmail.com)
    Description : User Views
"""

# System
from rest_framework import status
from rest_framework.viewsets import ViewSet
from drf_spectacular.utils import extend_schema

# Project
from core.constants import SYSTEM_CODE
from core.exception import raise_exception
from core.response import create_response
from apps.users.serializers import (
    SignUpSerializer,
    SignInSerializer,
    TokenRefreshSerializer,
)
from core.swagger import common_response_schema


@extend_schema(
    tags=["[Auth]"],
)
class AuthViewSet(ViewSet):
    """
    인증에 관련된 ViewSet 회원가입과 로그인을 처리함.
    """

    authentication_classes = []  # 인증 과정을 생략

    @extend_schema(
        summary="회원가입",
        request=SignUpSerializer,
    )
    @common_response_schema(status_code=201, description="회원가입 성공", serializer=SignUpSerializer)
    def sign_up(self, request):
        """
        회원가입을 처리합니다.
        """
        serializer = SignUpSerializer(data=request.data)

        # Validation Check
        if not serializer.is_valid():
            raise_exception(code=SYSTEM_CODE.INVALID_FORMAT)

        serializer.save()

        return create_response(data=serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="로그인",
        request=SignInSerializer,
    )
    @common_response_schema(status_code=200, description="로그인 성공", serializer=SignInSerializer)
    def sign_in(self, request):
        """
        로그인을 처리합니다.
        """
        serializer = SignInSerializer(data=request.data)

        # Validation Check
        if not serializer.is_valid():
            raise_exception(code=SYSTEM_CODE.INVALID_FORMAT)

        return create_response(data=serializer.data)

    @extend_schema(
        summary="토큰 재발급",
        request=TokenRefreshSerializer,
    )
    @common_response_schema(
        status_code=200,
        description="토큰 재발급 성공",
        serializer=TokenRefreshSerializer,
    )
    def token_refresh(self, request):
        """
        토큰 재발급을 처리합니다.
        """
        serializer = TokenRefreshSerializer(data=request.data)

        # Validation Check
        if not serializer.is_valid():
            raise_exception(code=SYSTEM_CODE.INVALID_FORMAT)

        return create_response(data=serializer.data)
