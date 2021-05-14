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

    dev_name = request.POST.get('dev_name')
    token = request.POST.get('token')
    isDeletion = request.POST.get('del')

    if request.method == "GET":
        data = {"message": "Добро пожаловать! Введите логин и пароль для получения токена.", "email": "", "token": ""}
        return render(request, "index.html", context=data)

    elif request.method == "POST":
        # add device
        if token and dev_name and not isDeletion:
            user = authenticate(token, False)
            d = Device(user_id=user.id, name=dev_name, quality=720, isReady=False)
            d.save()
            device = Device.objects.filter(user_id=user.id).values('id', 'name')
            data = {"message": "Устройство добавлено!", "device": device, "token": token}
            return render(request, "index.html", context=data)
        # remove device
        elif token and dev_name and isDeletion:
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
            return render(request, "index.html", context=data)

@csrf_exempt
def state(request):
    # find user by token
    user = authenticate(request, True)
    data = json.loads(request.body)
    dev_id = data['id']
    state = data['isReady']
    # set Ready flag
    dev = Device.objects.get(user_id=user.id, id=dev_id)
    dev.isReady = state
    dev.save()
    # build JSON
    serializer = DeviceSerializer(dev)
    device = JSONRenderer().render(serializer.data)
    return HttpResponse(device, content_type="application/json")

@csrf_exempt
def getConfig(request):
    user = authenticate(request, True)
    data = json.loads(request.body)
    dev_id = data['id']
    dev = Device.objects.get(user_id=user.id, id=dev_id)
    serializer = DeviceSerializer(dev)
    device_config = JSONRenderer().render(serializer.data)
    return HttpResponse(device_config)

def authenticate(value, isRequest):
    auth = JWTAuthentication
    if isRequest:
        return auth.authenticate(auth, request=value)
    else:
        return auth._authenticate_credentials(value)