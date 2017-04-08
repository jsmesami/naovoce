from django.contrib import admin
from django.contrib.sitemaps.views import sitemap as sitemap_view
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import RedirectView

import staticpage.views
import utils.views
import user.views
import naovoce.views

from . import feeds
from . import sitemap


urlpatterns = [
    url(r'^fruitadmin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^$', naovoce.views.home_view, name='home'),
    url(r'^api/v1/', include('naovoce.api.urls', namespace='api')),
    url(r'^herbarium/', include('fruit.herbarium.urls', namespace='herbarium')),
    url(r'^fruit/', include('fruit.urls', namespace='fruit')),
    url(r'^gallery/', include('gallery.urls', namespace='gallery')),
    url(r'^newsletter/', include('newsletter.urls', namespace='newsletter')),
    url(r'^pickers/', include('user.urls', namespace='pickers')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/$', user.views.accounts_profile),
    url(r'^feeds/fruit/', feeds.FruitFeed(), name='rss-fruit'),
    url(r'^sitemap\.xml$', sitemap_view, dict(sitemaps=sitemap.sitemaps), name='sitemap'),
    url(r'^robots\.txt$', utils.views.plain_text_view, dict(template_name='robots.txt'), name='robots'),
]

urlpatterns += i18n_patterns(
    '',
    url(r'^$', naovoce.views.home_view, name='home'),
    url(_(r'^map/$'), naovoce.views.map_view, name='map'),
    url(_(r'^media(?:/(?P<type_slug>[^/]+))?/$'), naovoce.views.media_view, name='media'),
    url(_(r'^codex/$'), staticpage.views.static_view,
        dict(template_name='staticpage/codex.html'), name='codex'),

    # TODO: Orphaneded URL, remove in mid 2017:
    url(_(r'^about-us/$'), RedirectView.as_view(permanent=True, pattern_name='team')),

    url(_(r'^our-team/$'), staticpage.views.static_view,
        dict(template_name='staticpage/team.html'), name='team'),
    url(_(r'^partners/$'), staticpage.views.static_view,
        dict(template_name='staticpage/partners.html'), name='partners'),

    url(
        _(r'^support-us/financially/$'),
        staticpage.views.static_view,
        dict(
            template_name='staticpage/support.html',
            additional_context=dict(section='financially'),
        ),
        name='support-financially',
    ),
    url(
        _(r'^support-us/engage/$'),
        staticpage.views.static_view,
        dict(
            template_name='staticpage/support.html',
            additional_context=dict(section='engage'),
        ),
        name='support-engage',
    ),
    url(
        _(r'^support-us/zoot/$'),
        staticpage.views.static_view,
        dict(
            template_name='staticpage/support.html',
            additional_context=dict(section='zoot'),
        ),
        name='support-zoot',
    ),

    url(_(r'^downloads/$'), staticpage.views.static_view, name='downloads'),
    url(_(r'^privacy-policy/$'), staticpage.views.static_view, name='privacy'),
    url(_(r'^prague-orchards-popularization/$'), staticpage.views.static_view,
        dict(template_name='staticpage/projects.html'), name='popularization'),
    url(_(r'^training-workshops/$'), staticpage.views.static_view,
        dict(template_name='staticpage/projects.html'), name='workshops'),
    url(_(r'^mapping-application-development/$'), staticpage.views.static_view,
        dict(template_name='staticpage/application.html'), name='app-devel'),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
