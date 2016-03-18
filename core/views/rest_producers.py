import json
import core.models as models
from .utils import success_response, error_response
from .utils import _get_title
from .decorators import inject_json_data, inject_lang


@inject_lang
def producers(request, lang):
    titles = models.ProducerTitle.objects.select_related()
    titles = titles.filter(lang=lang)

    if 'title' in request.GET:
        titles = titles.filter(
            title__istartswith=request.GET['title']
        )

    return success_response({
        'producers': [
            {
                'id': title.producer.id,
                'title': title.title,
                'ethical': title.producer.get_ethical()
            }
            for title in titles
        ]
    })
