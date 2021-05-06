from django.http import HttpResponse
from django.template import loader
import json
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status, exceptions
from .serializers import DeviceSerializer
from .models import Device
from authentication.models import User
from authentication.backends import JWTAuthentication

import io
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

from .forms import UserForm
from django.shortcuts import render

@csrf_exempt
def index(request): #set_readiness or set ready flag

    #json_str = ((request.body).decode('utf-8'))
    #json_obj = json.loads(json_str)
    #tok = json_str['token']

    # Определяем пользователя по токену
    auth = JWTAuthentication
    user = auth.authenticate(auth, request=request)
    #print(user.id)
    #d = Device(user_id=user, name = 'Remote PC', quality = 720, isReady = False)
    #d.save()

    # Выставляем флаг готовности
    dev = Device.objects.get(user_id=user)
    dev.isReady = True
    dev.save()
    #print(dev)
    if dev.isReady:
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
def getConfig(request):
    auth = JWTAuthentication
    user = auth.authenticate(auth, request=request)
    dev = Device.objects.get(user_id=user)
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

def auth(request):
    form = UserForm()
    return render(request, 'auth.html', {'form': form})