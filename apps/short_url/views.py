"""
    Copyright ⓒ 2024 Dcho, Inc. All Rights Reserved.
    Author : Dcho (tmdgns743@gmail.com)
    Description : Short URL View
"""

# System
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.viewsets import ViewSet
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework.permissions import IsAuthenticated, AllowAny


# Project
from core.constants import SYSTEM_CODE
from core.exception import raise_exception
from core.response import create_response
from core.swagger import common_response_schema
from apps.short_url.serializers import (
    ShortURLSerializer,
    ShortURLRedirectSerializer,
    ShortURLDeleteSerializer,
    ShortURLVisitSerializer,
)


@extend_schema(
    tags=["[Short URL]"],
)
class ShortURLViewSet(ViewSet):
    """
    Short URL에 관련된 ViewSet
    """

    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        API별 Permission 설정
        """
        if self.action == "get_redirect":
            return [AllowAny()]
        return super().get_permissions()

    @extend_schema(
        summary="Short URL 생성",
        request=ShortURLSerializer,
    )
    @common_response_schema(
        status_code=201,
        description="Short URL 생성 성공",
        serializer=ShortURLSerializer,
    )
    def post_short_url(self, request):
        """
        Short URL 생성 API
        """

        serializer = ShortURLSerializer(data=request.data, context={"request": request})

        # Validation Check
        if not serializer.is_valid():
            raise_exception(code=SYSTEM_CODE.INVALID_FORMAT)

        serializer.save()

        return create_response(data=serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Short URL 조회(Redirect)",
        parameters=[
            OpenApiParameter(name="url", description="Short URL", type=str, location="path"),
        ],
        responses={
            302: OpenApiResponse(
                description="원본 URL로 Redirect 성공",
            ),
        },
    )
    def get_redirect(self, request, url):
        """
        Short URL을 Redirect 하는 API
        localhost:8000/{short_url}로 접속하면 Redirect
        """

        serializer = ShortURLRedirectSerializer(data={"request_url": url}, context={"request": request})
        # Validation Check
        if not serializer.is_valid():
            raise_exception(code=SYSTEM_CODE.INVALID_FORMAT)
        original_url = serializer.save()

        return redirect(original_url)

    @extend_schema(
        summary="Short URL 삭제",
        parameters=[
            OpenApiParameter(name="url", description="Short URL", type=str, location="path"),
        ],
    )
    @common_response_schema(
        status_code=204,
        description="Short URL 삭제 성공",
    )
    def delete_short_url(self, request, url):
        """
        Short URL 삭제 API
        """

        serializer = ShortURLDeleteSerializer(data={"request_url": url}, context={"request": request})

        # Validation Check
        if not serializer.is_valid():
            raise_exception(code=SYSTEM_CODE.INVALID_FORMAT)

        serializer.save()

        return create_response(status=status.HTTP_204_NO_CONTENT)

    def get_visit_short_url(self, request, url):
        """
        Short URL 통계 조회 API
        """

        print("url: ", url)

        serializer = ShortURLVisitSerializer(data={"request_url": url}, context={"request": request})

        # Validation Check
        if not serializer.is_valid():
            raise_exception(code=SYSTEM_CODE.INVALID_FORMAT)

        return create_response(data=serializer.data, status=status.HTTP_200_OK)
