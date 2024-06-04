"""URL Configuration for hardboiledegg"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from asset import urls as asset_urls
from hardboiledegg.views import HomeView
from user import urls as user_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(user_urls)),
    path("", include(asset_urls)),
    path("", HomeView.as_view(), name="home"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
