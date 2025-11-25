"""URL Configuration for core"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from asset import urls as asset_urls
from attachment import urls as attachment_urls
from core.views import HomeView
from user import urls as user_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(user_urls)),
    path("", include(asset_urls)),
    path("", HomeView.as_view(), name="home"),
    path("", include(attachment_urls)),
]

# Serve media files in all environments
# In Docker, Nginx serves these before they reach Django
# In Windows, Django serves them directly
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
