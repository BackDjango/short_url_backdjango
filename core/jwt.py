"""
    Copyright ⓒ 2024 Dcho, Inc. All Rights Reserved.
    Author : Dcho (tmdgns743@gmail.com)
    Description : Custom JWT
"""

# System
import jwt
from datetime import datetime, timezone, timedelta
from django.conf import settings
from rest_framework import status
from rest_framework.authentication import BaseAuthentication

# Project
from core.constants import SERVICE, SYSTEM_CODE
from core.exception import raise_exception
from apps.users.models import User


class CustomJWTAuthentication(BaseAuthentication):
    """
    Custom JWT 인증에 관한 부분이므로, 인증시 해당 로직을 처리합니다.
    """

    def authenticate(self, request):
        """
        인증
        """
        authorization_header: str = request.headers.get("Authorization", None)

        if not authorization_header:
            return None

        access_token = authorization_header.split(" ")[-1]

        if not access_token:
            return None

        # 토큰 검증
        user = self.validate_token(access_token)

        return (user, None)

    @classmethod
    def validate_token(cls, token):
        """
        토큰 검증하는 함수
        """
        try:
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        # 토근 만료
        except jwt.ExpiredSignatureError:
            # TODO: request 의존성 제거
            raise_exception(code=SYSTEM_CODE.TOKEN_EXPIRED, status=status.HTTP_401_UNAUTHORIZED)
        # 토큰 부정확
        except jwt.DecodeError:
            raise_exception(code=SYSTEM_CODE.TOKEN_INVALID, status=status.HTTP_401_UNAUTHORIZED)

        user_id = decoded.get("user_id")

        user = User.objects.filter(id=user_id).first()

        # 존재 하지 않는 유저
        if not user:
            raise_exception(code=SYSTEM_CODE.USER_NOT_FOUND, status=status.HTTP_401_UNAUTHORIZED)
        # 활성화 되지 않은 유저
        if not user.is_active:
            raise_exception(code=SYSTEM_CODE.USER_NOT_ACTIVE, status=status.HTTP_401_UNAUTHORIZED)

        return user

    @classmethod
    def create_token(cls, user: User):
        """
        access, refresh token 생성하는 함수 입니다.
        """
        token = {
            "access_token": cls.create_access_token(user=user),
            "refresh_token": cls.create_refresh_token(user=user),
        }
        return token

    @classmethod
    def get_payload(cls, user: User, _exp):
        """
        payload 생성
        """
        exp = datetime.now(tz=timezone.utc) + _exp
        payload = {
            "user_id": user.id,
            "email": user.email,
            "exp": exp,
            "iat": datetime.now(tz=timezone.utc),
        }
        return payload

    @classmethod
    def create_access_token(cls, user: User):
        """
        Access Token 생성
        """
        payload = cls.get_payload(user=user, _exp=timedelta(minutes=SERVICE.ACCESS_TOKEN_EXP_MIN))
        access_token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm="HS256")
        return access_token

    @classmethod
    def create_refresh_token(cls, user: User):
        """
        Refresh Token 생성
        """
        payload = cls.get_payload(user=user, _exp=timedelta(days=SERVICE.REFRESH_TOKEN_EXP_DAY))
        refresh_token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm="HS256")
        return refresh_token

    @classmethod
    def create_test_token(cls, user: User):
        """
        Access Token 생성
        """
        payload = cls.get_payload(user=user, _exp=timedelta(seconds=0))
        test_token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm="HS256")
        return test_token
