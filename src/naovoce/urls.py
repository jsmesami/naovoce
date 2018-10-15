from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

app_name = "naovoce"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('naovoce.api.v1.urls', namespace='api')),  # Legacy API
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
