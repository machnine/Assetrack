"""user urls"""
from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy

from .views import UserLoginView, UserPasswordChangeView

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page=reverse_lazy("login")), name="logout"),
    path("password_change/", UserPasswordChangeView.as_view(), name="password_change"),
]
