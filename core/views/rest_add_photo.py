import json
import core.models as models
from django.views.decorators.csrf import csrf_exempt
from .utils import success_response, error_response
from .decorators import inject_json_data, inject_lang


@csrf_exempt
def add_photo(request, product_id):
    product = models.Product.objects.filter(id=product_id).first()

    if not product:
        return error_response({'error': 'Not found.'}, status=404)

    for name, photo in request.FILES.items():
        product_photo = models.ProductPhoto(product=product, image=photo)
        product_photo.save()
        return success_response({'photo': product_photo.get_url()})

    return error_response({'error': 'No image was sent.'}, status=400)
