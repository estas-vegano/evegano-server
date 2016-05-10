import json
import core.models as models
import core.err_codes as err_codes
from django.views.decorators.csrf import csrf_exempt
from .utils import success_response, error_response
from .decorators import inject_json_data, inject_lang


@csrf_exempt
def add_photo(request, product_id):
    product = models.Product.objects.filter(id=product_id).first()

    if not product:
        return error_response(err_codes.PRODUCT_NOT_FOUND,
                              'Product not found.')

    for name, photo in request.FILES.items():
        product_photo = models.ProductPhoto(product=product, image=photo)
        product_photo.save()
        return success_response({'url': product_photo.get_url()})

    return error_response(err_codes.NO_IMAGE, 'No image was sent.')
