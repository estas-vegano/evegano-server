def category(request, id):
    lang = _get_lang(request)
    category_obj = models.Category.objects.get(id=id)

    return success_response({
        'id': category_obj.id,
        'title': category_obj.get_title(lang),
        'children': {
            c.id: _get_title(c, lang)
            for c in models.Category.objects.filter(parent=category_obj)
        }
    })
