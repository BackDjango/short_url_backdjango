"""
    Copyright ⓒ 2024 Dcho, Inc. All Rights Reserved.
    Author : Dcho (tmdgns743@gmail.com)
    Description : Short URL Model
"""

# System
from django.db import models

# Project
from core.models import BaseModel


class ShortURL(BaseModel):
    """
    Short URL 모델입니다.
    """

    url = models.URLField(verbose_name="origin url")
    hash_value = models.CharField(max_length=100, verbose_name="hash value")
    request_count = models.IntegerField(default=0, verbose_name="요청 횟수")
    expiration_date = models.DateTimeField(null=True, blank=True, verbose_name="만료일시")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="삭제일시")

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="short_urls",
    )

    class Meta:
        db_table = "short_url"


class Visit(BaseModel):
    """
    방문자 추적을 위한 Visit 모델입니다.
    """

    referrer = models.URLField(null=True, blank=True, verbose_name="referrer URL")

    short_url = models.ForeignKey(
        "short_url.ShortURL",
        on_delete=models.CASCADE,
        related_name="visits",
    )

    class Meta:
        db_table = "visit"
