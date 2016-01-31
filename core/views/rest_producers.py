def producers(request):
    lang = _get_lang(request)
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
                'ethical': title.producer.ethical
            }
            for title in titles
        ]
    })
