from django.http import HttpResponse, HttpRequest
from django.template import loader
import json
import requests
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status, exceptions
from .serializers import DeviceSerializer
from .models import Device
from authentication.models import User
from authentication.backends import JWTAuthentication
from authentication.serializers import UserSerializer, LoginSerializer
from django.core.serializers.json import DjangoJSONEncoder

import io
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render

@csrf_exempt
def main(request):

    serializer_class = LoginSerializer

    dev_name = request.POST.get('dev_name')
    token = request.POST.get('token')
    flag = request.POST.get('add')

    if request.method == "GET":
        data = {"message": "Добро пожаловать! Введите логин и пароль для получения токена.", "email": "", "token": ""}
        return render(request, "index.html", context=data)
    # add device
    elif token and dev_name and flag:
        user = authenticate(token, False)
        d = Device(user_id=user.id, name=dev_name, quality=720, isReady=False)
        d.save()
        device = Device.objects.filter(user_id=user.id).values('id', 'name')
        data = {"message": "Устройство добавлено!", "device": device, "token": token}
        return render(request, "index.html", context=data)
    # remove device
    elif token and dev_name and not flag:
        user = authenticate(token, False)
        d = Device.objects.filter(user_id=user.id, name=dev_name)
        d.delete()
        device = Device.objects.filter(user_id=user.id).values('id', 'name')
        data = {"message": "Устройство удалено!", "device": device, "token": token}
        return render(request, "index.html", context=data)
    # show device list
    elif token and not dev_name:
        user = authenticate(token, False)
        device = Device.objects.filter(user_id=user.id).values('id', 'name')
        data = {"message": "Список устройств получен!", "device": device, "token": token}
        print(device)
        return render(request, "index.html", context=data)
    # login
    else:
        response_json = json.dumps(request.POST)
        load = json.loads(response_json)
        serializer = serializer_class(data=load)
        serializer.is_valid(raise_exception=True)
        token = serializer.data['token']
        username = serializer.data['username']
        return HttpResponse(json.dumps({"username": username, "token": token}), content_type="application/json")

@csrf_exempt
def start(request):

    # Определяем пользователя по токену
    user = authenticate(request, True)

    # Выставляем флаг готовности
    dev = Device.objects.get(user_id=user.id, id=9)
    dev.isReady = True
    dev.save()
    # Строим JSON ответ
    try:
        serializer = DeviceSerializer(dev)
        remote_device = JSONRenderer().render(serializer.data)
    except ValueError:
        return JsonResponse({
            'error': 'bla bla bla',
        })
    return HttpResponse(remote_device)

@csrf_exempt
def stop(request):
    user = authenticate(request, True)
    dev = Device.objects.get(user_id=user.id, id=9)
    dev.isReady = False
    dev.save()
    try:
        serializer = DeviceSerializer(dev)
        remote_device = JSONRenderer().render(serializer.data)
    except ValueError:
        return JsonResponse({
            'error': 'bla bla bla',
        })
    return HttpResponse(remote_device)

@csrf_exempt
def getConfig(request):

    user = authenticate(request, True)
    dev = Device.objects.get(user_id=user.id, id=9)
    #dev.quality = 720
    #dev.save()

    try:
        serializer = DeviceSerializer(dev)
        device_config = JSONRenderer().render(serializer.data)
    except ValueError:
        return JsonResponse({
            'error': 'bla bla bla',
        })

    return HttpResponse(device_config)

def authenticate(value, isRequest):
    auth = JWTAuthentication
    if isRequest:
        return auth.authenticate(auth, request=value)
    else:
        return auth._authenticate_credentials(value)