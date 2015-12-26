from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import core.models as models


def product_json(product_id, lang):
    product = models.Product.objects.select_related()\
                                    .filter(id=product_id)\
                                    .first()
    result = {
        'id': product.id,
        'title': product.get_title(lang),
        'info': product.info,
        'photo': product.get_photo_url(),
        'producer': {'id': product.producer.id,
                     'title': product.producer.get_title(lang),
                     'ethical': product.producer.ethical},
    }
    category = product.category.get_json_tree(lang)
    if product.category.parent:
        category_parent = product.category.parent.get_json_tree(lang)
        category_parent['sub'] = category
        result['category'] = category_parent
    else:
        result['category'] = category

    return result


def check(request):
    if hasattr(request, 'LANGUAGE_CODE'):
        lang = request.LANGUAGE_CODE
    else:
        lang = settings.DEFAULT_LANGUAGE

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
    if hasattr(request, 'LANGUAGE_CODE'):
        lang = request.LANGUAGE_CODE
    else:
        lang = settings.DEFAULT_LANGUAGE

    return JsonResponse({
        'categories': {
            c.id: _get_title(c, lang)
            for c in models.Category.objects.filter(parent__isnull=True)
        }
    })


def category(request, id):
    if hasattr(request, 'LANGUAGE_CODE'):
        lang = request.LANGUAGE_CODE
    else:
        lang = settings.DEFAULT_LANGUAGE

    category_obj = models.Category.objects.get(id=id)

    return JsonResponse({
        'title': category_obj.get_title(lang),
        'children': {
            c.id: _get_title(c, lang)
            for c in models.Category.objects.filter(parent=category_obj)
        }
    })
