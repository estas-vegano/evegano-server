def categories(request):
    lang = _get_lang(request)

    return success_response({
        c.id: _get_title(c, lang)
        for c in models.Category.objects.filter(parent__isnull=True)
    })
