import json
import core.models as models
from .utils import success_response, error_response
from .decorators import inject_json_data, inject_lang


@inject_json_data
@inject_lang
def add(request, lang, json_data):
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
    return success_response(product.to_dict(lang))
