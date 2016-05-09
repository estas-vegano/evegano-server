import json
from django.views.decorators.csrf import csrf_exempt
import core.models as models
import core.err_codes as err_codes
from .utils import success_response, error_response
from .decorators import inject_json_data, inject_lang


@csrf_exempt
@inject_json_data
@inject_lang
def add(request, lang, json_data):
    for item in ('title', 'info', 'code_type', 'code',
                 'producer_id', 'category_id'):
        if item not in json_data:
            return error_response(
                err_codes.WRONG_PARAMETERS,
                'Expected parameter {}'.format(item)
            )
    code_type, _ = models.CodeType.objects.get_or_create(
        name=json_data['code_type']
    )
    if models.ProductCode\
             .objects\
             .filter(type=code_type, code=json_data['code'])\
             .first():
        return error_response(err_codes.PRODUCT_EXISTS,
                              'Product code already exists')

    producer = models.Producer.objects.get(id=json_data['producer_id'])
    category = models.Category.objects.get(id=json_data['category_id'])
    product = models.Product(
        info=json_data['info'],
        producer=producer,
        category=category,
    )
    product.save()
    title = models.ProductTitle(
        product=product,
        lang=lang,
        title=json_data['title']
    )
    title.save()
    code = models.ProductCode(
        product=product,
        type=code_type,
        code=json_data['code'],
    )
    code.save()
    return success_response(product.to_dict(lang))
