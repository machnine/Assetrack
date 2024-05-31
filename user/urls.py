"""user urls"""
from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy

from .views import UserLoginView

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page=reverse_lazy("login")), name="logout"),
]
