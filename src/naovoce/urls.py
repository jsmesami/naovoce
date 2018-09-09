from django.contrib import admin
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

app_name = "naovoce"

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include('naovoce.api.v1.urls', namespace='api')),  # Legacy API
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
