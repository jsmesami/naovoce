from django.contrib import admin
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

import utils.views
import user.views
import naovoce.views


urlpatterns = [
    # Legacy URLs redirects
    url(r'^gallery/blogpost\.*', RedirectView.as_view(permanent=True, url='/web/blog')),
    url(r'^herbarium\.*', RedirectView.as_view(permanent=True, url='/web/herbar')),
    url(r'^cs/$', RedirectView.as_view(permanent=True, url='/web')),
    url(r'^en/$', RedirectView.as_view(permanent=True, url='/web')),
    url(r'^cs/mapa/$', RedirectView.as_view(permanent=True, pattern_name='map')),
    url(r'^en/map/$', RedirectView.as_view(permanent=True, pattern_name='map')),
    url(r'^cs/kodex/$', RedirectView.as_view(permanent=True, url='/web/kodex')),
    url(r'^en/codex/$', RedirectView.as_view(permanent=True, url='/web/kodex')),

    url(r'^$', RedirectView.as_view(permanent=True, url='/web/')),
    url(r'^fruitadmin/', include(admin.site.urls)),
    url(r'^api/v1/', include('naovoce.api.urls', namespace='api')),
    url(r'^fruit/', include('fruit.urls', namespace='fruit')),
    url(r'^gallery/', include('gallery.urls', namespace='gallery')),
    url(r'^newsletter/', include('newsletter.urls', namespace='newsletter')),
    url(r'^pickers/', include('user.urls', namespace='pickers')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/$', user.views.accounts_profile),
    url(r'^robots\.txt$', utils.views.plain_text_view, dict(template_name='robots.txt'), name='robots'),
    url(r'^map/$', naovoce.views.map_view, name='map'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
