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

    def _generated_short_url(self, url, expiration_date=None):
        """
        Short URL 생성 및 반환 하는 내부 함수

        URL을 해싱하여 Short URL을 생성한다.
        만료일시가 존재하면 해당 일시까지 유효하다.
        생성 후 Base62 인코딩하여 반환한다.
        """
        hash_value = Algorithm.hash_url(url=url)

        short_url = ShortURL.objects.create(
            url=url,
            hash_value=hash_value,
            expiration_date=expiration_date,
            user=self.context["request"].user,
        )
        encoded = Algorithm.base62_encode(short_url.hash_value)

        return encoded

    def create(self, validated_data):
        """
        Short URL 생성
        """
        url = validated_data["url"]
        expiration_date = validated_data.get("expiration_date")

        encoded = self._generated_short_url(url, expiration_date)

        return {"encoded": encoded}


class ShortURLRedirectSerializer(serializers.Serializer):
    request_url = serializers.CharField(max_length=7, required=True, label="Short URL")

    def validate_request_url(self, data):
        decoded = Algorithm.base62_decode(data)

        short_url = ShortURL.objects.filter(hash_value=decoded, deleted_at=None).first()
        if not short_url:
            raise_exception(code=SYSTEM_CODE.SHORT_URL_NOT_FOUND)

        if short_url.expiration_date and short_url.expiration_date < datetime.now():
            raise_exception(code=SYSTEM_CODE.SHORT_URL_EXPIRED)
        return short_url

    def save(self):
        short_url = self.validated_data["request_url"]
        short_url.request_count += 1
        short_url.save()

        return short_url.url


class ShortURLDeleteSerializer(serializers.Serializer):
    request_url = serializers.CharField(max_length=7, required=True, label="Short URL")

    def validate_request_url(self, data):
        # Base62 디코딩
        decoded = Algorithm.base62_decode(data)

        short_url = ShortURL.objects.filter(hash_value=decoded, deleted_at=None, user=self.context["request"].user).first()

        # 존재 하지 않는 URL 처리
        if not short_url:
            raise_exception(code=SYSTEM_CODE.SHORT_URL_NOT_FOUND)
        return short_url

    def save(self):
        short_url = self.validated_data["request_url"]

        # 현재 시간으로 삭제 처리
        short_url.deleted_at = datetime.now()
        short_url.save()
        return None
