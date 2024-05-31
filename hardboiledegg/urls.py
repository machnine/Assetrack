"""URL Configuration for hardboiledegg"""

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
