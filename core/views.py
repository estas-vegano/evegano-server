from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import core.models as models


def _get_lang(request):
    if hasattr(request, 'LANGUAGE_CODE'):
        lang = request.LANGUAGE_CODE
    else:
        lang = settings.DEFAULT_LANGUAGE
    return lang


def product_json(product_id, lang):
    product = models.Product.objects.select_related()\
                                    .filter(id=product_id)\
                                    .first()
    return product.to_dict(lang)


def check(request):
    lang = _get_lang(request)

    if 'code' not in request.GET or 'type' not in request.GET:
        return JsonResponse({'error': 'Expected args: code, type'})

    code = models.ProductCode.objects\
                             .filter(code=request.GET['code'],
                                     type=request.GET['type'])\
                             .first()
    if not code:
        return JsonResponse({'error': 'Not found'})

    return JsonResponse(product_json(code.product.id, lang))


def add(request):
    pass


def _get_title(category, lang):
    o = category.categorytitle_set.filter(lang=lang).first()
    if o:
        return o.title


def categories(request):
    lang = _get_lang(request)

    return JsonResponse({
        c.id: _get_title(c, lang)
        for c in models.Category.objects.filter(parent__isnull=True)
    })


def category(request, id):
    lang = _get_lang(request)
    category_obj = models.Category.objects.get(id=id)

    return JsonResponse({
        'id': category_obj.id,
        'title': category_obj.get_title(lang),
        'children': {
            c.id: _get_title(c, lang)
            for c in models.Category.objects.filter(parent=category_obj)
        }
    })


def producers(request):
    lang = _get_lang(request)
    titles = models.ProducerTitle.objects.select_related()
    titles = titles.filter(lang=lang)

    if 'title' in request.GET:
        titles = titles.filter(
            title__istartswith=request.GET['title']
        )

    return JsonResponse({
        'producers': [
            {
                'id': title.producer.id,
                'title': title.title,
                'ethical': title.producer.ethical
            }
            for title in titles
        ]
    })
