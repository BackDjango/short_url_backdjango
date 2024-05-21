"""
    Copyright ⓒ 2024 Dcho, Inc. All Rights Reserved.
    Author : Dcho (tmdgns743@gmail.com)
    Description : ShortURL Get Redirect Test
"""

# System
from django.urls import reverse
from rest_framework.test import APITestCase

# Project
from core.constants import SYSTEM_CODE
from core.algorithm import Algorithm
from apps.users.models import User

from apps.short_url.models import ShortURL


class GetRedirectTest(APITestCase):
    """
    단축 URL 조회(Redirect) 테스트
    """

    reverse_url = "get-redirect"

    origin_url = "https://www.google.com"

    @classmethod
    def setUpTestData(cls):
        # 유저 생성
        email = "test@test.com"
        password = "password1234"
        user = User.objects.create_user(email=email, password=password)

        # URL 생성
        cls.hash_value = Algorithm.hash_url(cls.origin_url)
        cls.short_url = ShortURL.objects.create(
            url=cls.origin_url,
            hash_value=cls.hash_value,
            user=user,
        )
        cls.encoded = Algorithm.base62_encode(cls.short_url.hash_value)

    # 단축 URL 리다이렉트 성공
    def test_get_redirect_success(self):
        url = reverse(self.reverse_url, kwargs={"url": self.encoded})
        response = self.client.get(path=url)

        self.assertEqual(response.status_code, 302)

    # 단축 URL 리다이렉트 실패 (존재하지 않는 URL)
    def test_get_redirect_not_found(self):
        encoded = self.encoded[:-1]
        url = reverse(self.reverse_url, kwargs={"url": encoded})
        response = self.client.get(path=url)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["code"], SYSTEM_CODE.SHORT_URL_NOT_FOUND[0])

    # 단축 URL 리다이렉트 실패 (만료된 URL)
    def test_get_redirect_expired(self):
        self.short_url.expiration_date = "2023-01-01"
        self.short_url.save()

        url = reverse(self.reverse_url, kwargs={"url": self.encoded})
        response = self.client.get(path=url)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["code"], SYSTEM_CODE.SHORT_URL_EXPIRED[0])
