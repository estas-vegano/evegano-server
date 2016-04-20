import json
import core.models as models
from django.views.decorators.csrf import csrf_exempt
from .utils import success_response, error_response
from .decorators import inject_lang, inject_json_data, require_params


@inject_lang
@csrf_exempt
@inject_json_data
@require_params('message')
def complain(request, lang, json_data):
    complain = models.Complain(lang=lang, message=json_data['message'])
    complain.save()
    return success_response({})
