from django.contrib import admin

from .models import JobPosting, UserSaveForLater, JobProcess

# Register your models here. - This ways we can edit the models via /admin/
admin.site.register(JobPosting)
admin.site.register(UserSaveForLater)
admin.site.register(JobProcess)
