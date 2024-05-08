"""
    Copyright ⓒ 2024 Dcho, Inc. All Rights Reserved.
    Author : Dcho (tmdgns743@gmail.com)
    Description : User Token Refresh Test
"""

# System
from django.urls import reverse
from rest_framework.test import APITestCase

# Project
from core.jwt import CustomJWTAuthentication
from core.constants import SYSTEM_CODE
from apps.users.models import User


class TokenRefreshTest(APITestCase):
    """
    Token 재발급 테스트
    """

    url = reverse("api-users:token-refresh")

    email = "test@test.com"
    password = "password1234"

    @classmethod
    def setUpTestData(cls):
        cls.data = {"email": cls.email, "password": cls.password}
        cls.user = User.objects.create_user(email="test@test.com", password="password1234")
        cls.user_access_token = CustomJWTAuthentication.create_access_token(user=cls.user)
        cls.user_refresh_token = CustomJWTAuthentication.create_refresh_token(user=cls.user)
        cls.expired_token = CustomJWTAuthentication.create_test_token(user=cls.user)

    # Token 재발급 성공
    def test_token_refresh_success(self):
        response = self.client.post(
            path=self.url,
            HTTP_AUTHORIZATION=f"Bearer {self.user_access_token}",
            data={"token": self.user_refresh_token},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["data"]["access_token"])
        self.assertTrue(response.data["data"]["refresh_token"])
        self.assertEqual(response.data["code"], SYSTEM_CODE.SUCCESS[0])

    # Token 재발급 실패 (값이 빈 값일 경우)
    def test_token_refresh_blank(self):
        response = self.client.post(
            path=self.url,
            HTTP_AUTHORIZATION=f"Bearer {self.user_access_token}",
            data={},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["code"], SYSTEM_CODE.INVALID_FORMAT[0])

    # Token 재발급 실패 (토큰이 빈 값일 경우)
    def test_token_refresh_token_blank(self):
        response = self.client.post(
            path=self.url,
            HTTP_AUTHORIZATION=f"Bearer {self.user_access_token}",
            data={"token": ""},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["code"], SYSTEM_CODE.INVALID_FORMAT[0])

    # Token 재발급 실패 (토큰이 잘못된 값일 경우)
    def test_token_refresh_token_invalid(self):
        response = self.client.post(
            path=self.url,
            HTTP_AUTHORIZATION=f"Bearer {self.user_access_token}",
            data={"token": "invalid_token"},
            format="json",
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["code"], SYSTEM_CODE.TOKEN_INVALID[0])

    # Token 재발급 실패 (토큰이 만료된 값일 경우)
    def test_token_refresh_token_expired(self):
        response = self.client.post(
            path=self.url,
            HTTP_AUTHORIZATION=f"Bearer {self.user_access_token}",
            data={"token": self.expired_token},
            format="json",
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["code"], SYSTEM_CODE.TOKEN_EXPIRED[0])

    # Token 재발급 실패 (존재하지 않는 유저일 경우)
    def test_token_refresh_user_not_exists(self):
        # 유저 삭제
        self.user.delete()

        response = self.client.post(
            path=self.url,
            HTTP_AUTHORIZATION=f"Bearer {self.user_access_token}",
            data={"token": self.user_refresh_token},
            format="json",
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["code"], SYSTEM_CODE.USER_NOT_FOUND[0])

    # Token 재발급 실패 (비활성화된 유저일 경우)
    def test_token_refresh_user_not_active(self):
        user = self.user
        user.is_active = False
        user.save()

        response = self.client.post(
            path=self.url,
            HTTP_AUTHORIZATION=f"Bearer {self.user_access_token}",
            data={"token": self.user_refresh_token},
            format="json",
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["code"], SYSTEM_CODE.USER_NOT_ACTIVE[0])
