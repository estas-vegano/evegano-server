import json
import core.models as models
from .utils import success_response, error_response
from .utils import _get_title
from .decorators import inject_json_data, inject_lang


@inject_lang
def category(request, lang, id):
    category_obj = models.Category.objects.filter(id=id).first()

    if not category_obj:
        return error_response({'error': 'Not found.'}, status=404)


    return success_response({
        'id': category_obj.id,
        'title': category_obj.get_title(lang),
        'children': [
            {'id': c.id,  'title': _get_title(c, lang)}
            for c in models.Category.objects\
                .filter(parent=category_obj)\
                .order_by('id')
        ]
    })
