from django.contrib import admin

from .models import JobPosting

# Register your models here. - This ways we can edit the models via /admin/
admin.site.register(JobPosting)