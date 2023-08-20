from rest_framework import generics, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from django.contrib.auth import login, authenticate

from .serializers import (
    EntryAuthSertializer,
    AuthSerializer,
    UserDetailSerializer,
)


class EntryAuthView(generics.GenericAPIView):
    serializer_class = EntryAuthSertializer
    permission_classes = [
        permissions.AllowAny,
    ]

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


class AuthView(generics.GenericAPIView):
    serializer_class = AuthSerializer
    permission_classes = [
        permissions.AllowAny,
    ]

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                phone_number=serializer.data.get("phone_number"),
                code=serializer.data.get("code"),
            )
            login(request, user)
            return Response(serializer.data)


class UserProfileView(generics.GenericAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(
            request.user, data=request, many=True
        )
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
