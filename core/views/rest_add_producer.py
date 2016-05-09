import json
from django.views.decorators.csrf import csrf_exempt
import core.models as models
import core.err_codes as err_codes
from .utils import success_response, error_response
from .decorators import inject_json_data, inject_lang


@csrf_exempt
@inject_lang
@inject_json_data
def add_producer(request, lang, json_data):
    if json_data.get('ethical') and \
       json_data['ethical'] not in models.BOOL2ETHICAL.keys():
        return error_response(err_codes.WRONG_PARAMETER_VALUE,
                              'The parameter ethical should be bool or null')

    producer = models.Producer.create(lang, json_data)
    return success_response(producer.get_dict(lang))
