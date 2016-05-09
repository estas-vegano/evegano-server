import json
import core.models as models
from django.views.decorators.csrf import csrf_exempt
from .utils import success_response, error_response
from .decorators import inject_lang, inject_json_data, require_params
import core.err_codes as err_codes


@inject_lang
@csrf_exempt
@inject_json_data
@require_params('message')
def complain(request, product_id, lang, json_data):
    product = models.Product.objects.filter(id=product_id).first()
    if not product:
        return error_response(err_codes.PRODUCT_NOT_FOUND,
                              'Product code not found.')

    complain = models.Complain(
        product=product,
        lang=lang,
        message=json_data['message']
    )
    complain.save()
    return success_response(None)
