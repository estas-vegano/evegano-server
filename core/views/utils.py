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


def error_response(data, status):
    return JsonResponse(data, status=status)

def success_response(data):
    return JsonResponse(data)
