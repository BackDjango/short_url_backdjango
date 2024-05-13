"""
    Copyright ⓒ 2024 Dcho, Inc. All Rights Reserved.
    Author : Dcho (tmdgns743@gmail.com)
    Description : Short URL Serializers
"""

# System
from datetime import datetime
from rest_framework import serializers

# Project
from core.constants import SYSTEM_CODE
from core.exception import raise_exception
from core.algorithm import Algorithm
from apps.short_url.models import ShortURL


class ShortURLSerializer(serializers.Serializer):
    url = serializers.URLField(required=True, write_only=True, label="[Input]Original URL")
    expiration_date = serializers.DateTimeField(required=False, write_only=True, label="[Input]만료일시")

    encoded = serializers.CharField(read_only=True, label="[Output]Short URL")

    def validate_url(self, data):
        """
        URL 유효성 검증
        """
        if ShortURL.objects.filter(url=data, deleted_at=None).exists():
            raise_exception(code=SYSTEM_CODE.URL_ALREADY)
        return data

    def validate_expiration_date(self, data):
        """
        만료일시 유효성 검증
        """
        if data and data < datetime.now():
            raise_exception(code=SYSTEM_CODE.EXPIRATION_DATE_INVALID)
        return data

    def create(self, validated_data):
        url = validated_data["url"]
        expiration_date = validated_data.get("expiration_date")

        # URL 해시값 생성
        hash_value = Algorithm.hash_url(url=url)

        # Short URL 생성
        short_url = ShortURL.objects.create(
            url=url,
            hash_value=hash_value,
            expiration_date=expiration_date,
            user=self.context["request"].user,
        )

        # Base62 인코딩
        encoded = Algorithm.base62_encode(short_url.hash_value)

        return {"encoded": encoded}
