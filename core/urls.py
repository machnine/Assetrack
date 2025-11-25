"""URL Configuration for core"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

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

# Serve media files in production
# Django's static() helper only works with DEBUG=True, so we add the pattern manually
# In Docker: Nginx intercepts /media/* before it reaches Django (efficient)
# In Windows: Django serves media files directly (simple, works out of the box)
if settings.MEDIA_URL and settings.MEDIA_ROOT:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]

if settings.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
