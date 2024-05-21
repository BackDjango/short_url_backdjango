"""
    Copyright ⓒ 2024 Dcho, Inc. All Rights Reserved.
    Author : Dcho (tmdgns743@gmail.com)
    Description : ShortURL Post ShortURL Test
"""

# System
from django.urls import reverse
from rest_framework.test import APITestCase

# Project
from core.constants import SYSTEM_CODE
from core.jwt import CustomJWTAuthentication
from apps.users.models import User
from apps.short_url.models import ShortURL


class PostShortURLTest(APITestCase):
    """
    단축 URL 생성 테스트
    """

    url = reverse("api-short-url:post-short-url")

    origin_url = "https://www.google.com"

    email = "test@test.com"
    password = "password1234"

    @classmethod
    def setUpTestData(cls):
        # 유저 생성
        cls.user = User.objects.create_user(email=cls.email, password=cls.password)
        cls.user_access_token = CustomJWTAuthentication.create_access_token(user=cls.user)

    # 단축 URL 생성 성공
    def test_post_short_url_success(self):
        data = {"url": self.origin_url}
        response = self.client.post(
            path=self.url,
            HTTP_AUTHORIZATION=f"Bearer {self.user_access_token}",
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["data"]["encoded"])
        self.assertEqual(response.data["code"], SYSTEM_CODE.SUCCESS[0])

    # 단축 URL 생성 실패 (유저 인증 실패)
    def test_post_short_url_unauthorized(self):
        data = {"url": self.origin_url}
        response = self.client.post(
            path=self.url,
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, 403)

    # 단축 URL 생성 실패 (값이 빈 값일 경우)
    def test_post_short_url_blank(self):
        data = {}
        response = self.client.post(
            path=self.url,
            HTTP_AUTHORIZATION=f"Bearer {self.user_access_token}",
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["code"], SYSTEM_CODE.INVALID_FORMAT[0])

    # 단축 URL 생성 실패 (URL이 빈 값일 경우)
    def test_post_short_url_url_blank(self):
        data = {"url": ""}
        response = self.client.post(
            path=self.url,
            HTTP_AUTHORIZATION=f"Bearer {self.user_access_token}",
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["code"], SYSTEM_CODE.INVALID_FORMAT[0])

    # 단축 URL 생성 실패 (URL이 이미 존재할 경우)
    def test_post_short_url_url_exists(self):
        ShortURL.objects.create(url=self.origin_url, user=self.user)
        data = {"url": self.origin_url}
        response = self.client.post(
            path=self.url,
            HTTP_AUTHORIZATION=f"Bearer {self.user_access_token}",
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["code"], SYSTEM_CODE.URL_ALREADY[0])

    # 단축 URL 생성 실패 (만료일시 유효하지 않은 경우)
    def test_post_short_url_expired(self):
        data = {"url": self.origin_url, "expiration_date": "2021-01-01"}
        response = self.client.post(
            path=self.url,
            HTTP_AUTHORIZATION=f"Bearer {self.user_access_token}",
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["code"], SYSTEM_CODE.EXPIRATION_DATE_INVALID[0])
