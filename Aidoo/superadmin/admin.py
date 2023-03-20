from django.contrib import admin
from .models import Report, ReportTicket, ConflictResolution


# Enable editing these models via /admin/.
admin.site.register(Report)
admin.site.register(ReportTicket)
admin.site.register(ConflictResolution)
