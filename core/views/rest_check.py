from .decorators import inject_lang
from .utils import success_response, error_response
import core.models as models
import core.err_codes as err_codes


@inject_lang
def check(request, lang):

    if 'code' not in request.GET or 'type' not in request.GET:
        return error_response(err_codes.WRONG_PARAMETERS,
                              'Expected parameters: code, type.')

    code = models.ProductCode.objects\
                             .filter(code=request.GET['code'],
                                     type__name=request.GET['type'])\
                             .first()
    if not code:
        return error_response(err_codes.PRODUCT_NOT_FOUND,
                              'Product code not found.')

    return success_response(models.Product.dict_by_id(code.product.id, lang))
