from django.shortcuts import render

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView

from .serializers import (RegistrationSerializer, LoginSerializer, UserSerializer)
from .renderers import UserJSONRenderer

from django.http import HttpResponse

import json
import io

# Create your views here.

class RegistrationAPIView(APIView):

    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def get(self, request):
        if request.method == "GET":
            data = {"message": "Введите email, имя пользователя и пароль!"}
            return render(request, "regi.html", context=data)

    def post(self, request):
        if request.method == "POST":
            if request.is_ajax():
                user = json.loads(request.POST.get('user'))
                serializer = self.serializer_class(data=user)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return HttpResponse(json.dumps({"email": serializer.data.get('email')}), content_type="application/json")
            else:
                user = request.data.get('user', {})
                serializer = self.serializer_class(data=user)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        if request.is_ajax():
            user = json.loads(request.POST.get('user'))
            serializer = self.serializer_class(data=user)
            serializer.is_valid(raise_exception=True)
            username = serializer.data.get('username')
            token = serializer.data.get('token')
            return HttpResponse(json.dumps({"username": username, "token": token}), content_type="application/json")
        else:
            user = request.data.get('user', {})
            serializer = self.serializer_class(data=user)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # Здесь нечего валидировать или сохранять. Мы просто хотим, чтобы
        # сериализатор обрабатывал преобразования объекта User во что-то, что
        # можно привести к json и вернуть клиенту.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)