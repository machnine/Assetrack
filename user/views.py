"""User views."""

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.html import format_html


class UserLoginView(LoginView):
    """Basic login view."""

    template_name = "user/login.html"
    next_page = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        """Handle GET requests."""
        if request.user.is_authenticated:
            next_page = request.GET.get("next", self.next_page)
            messages.info(request, "You are already logged in.")
            return redirect(next_page)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        user = get_user_model().objects.get(username=username)
        display_name = user.first_name or user.username
        messages.success(self.request, format_html(f"Welcome back, <b>{display_name}</b>."))
        return super().form_valid(form)
