import os
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from core.views import check, add, categories, category
from django.views.generic import RedirectView


admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v[0-9.]+/categories/(?P<id>[0-9]+)', category),
    url(r'^api/v[0-9.]+/categories/', categories),
    url(r'^api/v[0-9.]+/check$', check),
    url(r'^api/v[0-9.]+/add$', add),
    url(r'^docs/$', RedirectView.as_view(url='/docs/index.html')),
] + static('docs/',
           document_root=os.path.join(settings.BASE_DIR,
                                      'docs/build/html'))
