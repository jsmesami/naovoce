from django.conf import settings

ALLOWED_URLPATTERS = getattr(settings, 'STATICPAGE_API_ALLOWED_URLPATTERNS', [])
