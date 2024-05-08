"""
    Copyright ⓒ 2024 Dcho, Inc. All Rights Reserved.
    Author : Dcho (tmdgns743@gmail.com)
    Description : User Sign In Test
"""

# System
from django.urls import reverse
from rest_framework.test import APITestCase

# Project
from core.constants import SYSTEM_CODE
from apps.users.models import User


class SignInTest(APITestCase):
    """
    로그인 테스트
    """

    url = reverse("api-users:sign-in")

    email = "test@test.com"
    password = "password1234"

    @classmethod
    def setUpTestData(cls):
        cls.data = {"email": cls.email, "password": cls.password}
        user = User.objects.create_user(email="test@test.com", password="password1234")

    # 로그인 성공
    def test_sign_in_success(self):
        response = self.client.post(
            path=self.url,
            data=self.data,
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["data"]["access_token"])
        self.assertTrue(response.data["data"]["refresh_token"])
        self.assertEqual(response.data["code"], SYSTEM_CODE.SUCCESS[0])

    # 로그인 실패 (값이 빈 값일 경우)
    def test_sign_in_blank(self):
        data = {}
        response = self.client.post(
            path=self.url,
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["code"], SYSTEM_CODE.INVALID_FORMAT[0])

    # 로그인 실패 (이메일이 빈 값일 경우)
    def test_sign_in_email_blank(self):
        data = {"password": self.password}
        response = self.client.post(
            path=self.url,
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["code"], SYSTEM_CODE.INVALID_FORMAT[0])

    # 로그인 실패 (비밀번호가 빈 값일 경우)
    def test_sign_in_password_blank(self):
        data = {"email": self.email}
        response = self.client.post(
            path=self.url,
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["code"], SYSTEM_CODE.INVALID_FORMAT[0])

    # 로그인 실패 (존재하지 않는 이메일일 경우)
    def test_sign_in_email_not_exists(self):
        data = {"email": "test2@test.com", "password": self.password}
        response = self.client.post(
            path=self.url,
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["code"], SYSTEM_CODE.USER_NOT_FOUND[0])

    # 로그인 실패 (비밀번호가 틀릴 경우)
    def test_sign_in_password_invalid(self):
        data = {"email": self.email, "password": "password12345"}
        response = self.client.post(
            path=self.url,
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["code"], SYSTEM_CODE.USER_INVALID_PW[0])

    # 로그인 실패 (활성화 되지 않은 계정일 경우)
    def test_sign_in_not_active(self):
        user = User.objects.get(email=self.email)
        user.is_active = False
        user.save()

        response = self.client.post(
            path=self.url,
            data=self.data,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["code"], SYSTEM_CODE.USER_NOT_ACTIVE[0])
