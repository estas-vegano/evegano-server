import json
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import core.models as models

def _get_title(category, lang):
    o = category.categorytitle_set.filter(lang=lang).first()
    if o:
        return o.title

def _get_lang(request):
    if hasattr(request, 'LANGUAGE_CODE'):
        lang = request.LANGUAGE_CODE
    else:
        lang = settings.DEFAULT_LANGUAGE
    return lang


def error_response(code, message):
    response = {
        'error_code': code,
        'error_message': message,
    }
    return JsonResponse(response)


def success_response(data):
    response = {
        'error_code': 0,
        'error_message': None,
        'result': data
    }
    return JsonResponse(response)
