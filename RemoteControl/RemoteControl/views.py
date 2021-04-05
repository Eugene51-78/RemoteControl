from django.http import HttpResponse
from django.template import loader
import json
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from .serializers import ModelSerializer
from .models import Model

import io
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):

    json_str = ((request.body).decode('utf-8'))
    print(json_str)
    json_obj = json.loads(json_str)
    print(json_obj)
    jwt = json_obj['token']
    print(jwt)

    try:
        m = Model(model_text=jwt, pub_date='25.11.2022')
        serializer = ModelSerializer(m)
        jsone = JSONRenderer().render(serializer.data)
    except ValueError:
        return JsonResponse({
            'error': 'bla bla bla',
        })
    return HttpResponse(jsone)

###
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)