"""
    Copyright ⓒ 2024 Dcho, Inc. All Rights Reserved.
    Author : Dcho (tmdgns743@gmail.com)
    Description : User Sign Up Test
"""

# System
from django.urls import reverse
from rest_framework.test import APITestCase

# Project
from core.constants import SYSTEM_CODE
from apps.users.models import User


class SignUpTest(APITestCase):
    """
    회원가입 테스트
    """

    url = reverse("api-users:sign-up")

    email = "test@test.com"
    password = "password1234"

    # 회원가입 성공
    def test_sign_up_success(self):
        data = {"email": self.email, "password": self.password}
        response = self.client.post(
            path=self.url,
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["data"]["access_token"])
        self.assertTrue(response.data["data"]["refresh_token"])
        self.assertEqual(response.data["code"], SYSTEM_CODE.SUCCESS[0])

    # 회원가입 실패 (값이 빈 값일 경우)
    def test_sign_up_blank(self):
        data = {}
        response = self.client.post(
            path=self.url,
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["code"], SYSTEM_CODE.INVALID_FORMAT[0])

    # 회원가입 실패 (이메일이 빈 값일 경우)
    def test_sign_up_email_blank(self):
        data = {"password": self.password}
        response = self.client.post(
            path=self.url,
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["code"], SYSTEM_CODE.INVALID_FORMAT[0])

    # 회원가입 실패 (비밀번호가 빈 값일 경우)
    def test_sign_up_password_blank(self):
        data = {"email": self.email}
        response = self.client.post(
            path=self.url,
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["code"], SYSTEM_CODE.INVALID_FORMAT[0])

    # 회원가입 실패 (이메일이 이미 존재할 경우)
    def test_sign_up_email_exists(self):
        user = User.objects.create_user(email=self.email, password=self.password)
        data = {"email": self.email, "password": self.password}
        response = self.client.post(
            path=self.url,
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["code"], SYSTEM_CODE.EMAIL_ALREADY[0])
