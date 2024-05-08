"""
    Copyright ⓒ 2024 Dcho, Inc. All Rights Reserved.
    Author : Dcho (tmdgns743@gmail.com)
    Description : User Manager Test
"""

# System
from django.test import TestCase
from django.contrib.auth import get_user_model

# Project


class UserManagerTest(TestCase):
    """
    회원가입 가정후 회원가입 함수 테스트 코드를 작성하려고 합니다.
    이메일과 패스워드를 입력받고, 회원가입이 정상적으로 잘 이뤄졌는지 체크
    """

    def test_create_user(self):
        email = "test@test.com"
        password = "password1234"

        user = get_user_model().objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        email = "admin@example.com"
        password = "password1234"

        super_user = get_user_model().objects.create_superuser(email=email, password=password)
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
