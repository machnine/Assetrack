"""request log models"""

from django.db import models


class RequestLog(models.Model):
    """log requests"""

    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    path = models.CharField(max_length=200)
    method = models.CharField(max_length=10)
    status_code = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.timestamp}\t{self.method:<8}\t{self.status_code}\t{self.ip_address}\t{self.path}"
