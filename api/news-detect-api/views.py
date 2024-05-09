from json import JSONDecoder
from django.http import JsonResponse
from model import predict

import re

def detect_fake(request):
    json = JSONDecoder()
    body = json.decode(request.body.decode('UTF-8'))
    text = body['text']
    
    return JsonResponse({ 'prediction': predict(text) }, safe=False)

