from .decorators import inject_lang
from .utils import success_response, error_response
import core.models as models

@inject_lang
def check(request, lang):

    if 'code' not in request.GET or 'type' not in request.GET:
        return error_response({'error': 'Expected args: code, type.'},
                              status=400)

    code = models.ProductCode.objects\
                             .filter(code=request.GET['code'],
                                     type__name=request.GET['type'])\
                             .first()
    if not code:
        return error_response({'error': 'Not found.'}, status=404)

    return success_response(models.Product.dict_by_id(code.product.id, lang))
