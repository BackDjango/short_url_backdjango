"""
    Copyright ⓒ 2024 Dcho, Inc. All Rights Reserved.
    Author : Dcho (tmdgns743@gmail.com)
    Description : Short URL Algorithm
"""

# System
import hashlib
import base62


class Algorithm:
    def __init__(self):
        pass

    @staticmethod
    def hash_url(url):
        """URL을 받아 SHA-256 해시를 생성하여 반환합니다."""
        # URL을 SHA-256 해시로 변환
        hash_object = hashlib.sha256(url.encode())

        # 16진수 해시로 변환
        hash_hex = hash_object.hexdigest()

        # 해시값의 앞 10자리만 사용
        hash_value = hash_hex[:10]
        return hash_value

    @staticmethod
    def base62_encode(hash_value):
        """16진수 해시를 Base62 인코딩하여 반환합니다."""

        # 16진수 문자열을 정수로 변환
        decimal_representation = int(hash_value, 16)

        # Base62 인코딩
        encoded = base62.encode(decimal_representation)

        return encoded

    @staticmethod
    def base62_decode(encoded):
        """Base62 인코딩된 문자열을 디코딩하여 원래의 16진수 해시로 반환합니다."""
        # Base62 디코딩
        decoded_int = base62.decode(encoded)

        # 정수를 16진수 문자열로 변환
        hash_value = hex(decoded_int)[2:]  # '0x' 접두어 제거

        return hash_value
