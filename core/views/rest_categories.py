import json
import core.models as models
from .utils import success_response, error_response
from .utils import _get_title
from .decorators import inject_json_data, inject_lang


@inject_lang
def categories(request, lang):

    return success_response({
        'categories': [
            {'id': c.id, 'title': _get_title(c, lang)}
            for c in models.Category.objects.filter(parent__isnull=True)
        ]
    })
