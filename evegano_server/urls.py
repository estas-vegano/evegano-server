import os
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.views.generic import RedirectView


import core.views as v

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v[0-9.]+/categories/(?P<id>[0-9]+)', v.category),
    url(r'^api/v[0-9.]+/categories/', v.categories),
    url(r'^api/v[0-9.]+/check$', v.check),
    url(r'^api/v[0-9.]+/add$', v.add),
    url(r'^api/v[0-9.]+/add-producer$', v.add_producer),
    url(r'^api/v[0-9.]+/producers/$', v.producers),
    url(r'^docs/$', RedirectView.as_view(url='/docs/index.html')),
] + static('docs/',
           document_root=os.path.join(settings.BASE_DIR,
                                      'docs/build/html'))
