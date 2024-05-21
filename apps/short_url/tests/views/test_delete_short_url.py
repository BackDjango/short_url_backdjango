"""
    Copyright ⓒ 2024 Dcho, Inc. All Rights Reserved.
    Author : Dcho (tmdgns743@gmail.com)
    Description : ShortURL Delete ShortURL Test
"""

# System
from django.urls import reverse
from rest_framework.test import APITestCase

# Project
from core.constants import SYSTEM_CODE
from core.algorithm import Algorithm
from core.jwt import CustomJWTAuthentication
from apps.users.models import User

from apps.short_url.models import ShortURL


class DeleteShortURLTest(APITestCase):
    """
    단축 URL 삭제 테스트
    """

    reverse_url = "api-short-url:delete-short-url"

    origin_url = "https://www.google.com"

    @classmethod
    def setUpTestData(cls):
        # 유저 생성
        email = "test@test.com"
        password = "password1234"
        user = User.objects.create_user(email=email, password=password)
        cls.user_access_token = CustomJWTAuthentication.create_access_token(user=user)

        # URL 생성
        cls.hash_value = Algorithm.hash_url(cls.origin_url)
        cls.short_url = ShortURL.objects.create(
            url=cls.origin_url,
            hash_value=cls.hash_value,
            user=user,
        )

        cls.encoded = Algorithm.base62_encode(cls.short_url.hash_value)

    # 단축 URL 삭제 성공
    def test_delete_short_url_success(self):
        url = reverse(self.reverse_url, kwargs={"url": self.encoded})
        response = self.client.delete(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.user_access_token}",
        )

        self.assertEqual(response.status_code, 204)

    # 단축 URL 삭제 실패 (존재하지 않는 URL)
    def test_delete_short_url_not_exist(self):
        encoded = self.encoded + "a"
        url = reverse(self.reverse_url, kwargs={"url": encoded})
        response = self.client.delete(
            path=url,
            HTTP_AUTHORIZATION=f"Bearer {self.user_access_token}",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["code"], SYSTEM_CODE.SHORT_URL_NOT_FOUND[0])
