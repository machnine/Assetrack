"""middleware"""

from django.utils.deprecation import MiddlewareMixin

from .models import RequestLog


class RequestLogMiddleware(MiddlewareMixin):
    """log requests"""

    def process_request(self, request):
        """log request"""
        if request.path.startswith("/admin"):
            return
        RequestLog.objects.create(
            ip_address=self.get_client_ip(request),
            path=request.path,
            method=request.method,
        )

    def process_response(self, request, response):
        """log response"""
        log = RequestLog.objects.latest("timestamp")
        log.status_code = response.status_code
        log.save()
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip