from django.contrib import admin

from .models import RequestLog


@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "method", "status_code", "ip_address", "path")
    search_fields = ("ip_address", "method", "path")
    list_filter = ("timestamp", "method", "status_code")

    def get_queryset(self, request):
        # Override get_queryset to handle empty querysets gracefully
        queryset = super().get_queryset(request)
        if not queryset.exists():
            return RequestLog.objects.none()  # Return an empty queryset
        return queryset
