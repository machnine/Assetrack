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


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
