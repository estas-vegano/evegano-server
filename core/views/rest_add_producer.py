import json
import core.models as models
from .utils import success_response, error_response
from .decorators import inject_json_data, inject_lang


@inject_lang
@inject_json_data
def add_producer(request, lang, json_data):
    producer = models.Producer.create(lang, json_data)
    return success_response(producer.get_dict(lang))
