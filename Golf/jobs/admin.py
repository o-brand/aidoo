from django.contrib import admin

from .models import Job, Bookmark, Application

# Register your models here. - This ways we can edit the models via /admin/
admin.site.register(Job)
admin.site.register(Bookmark)
admin.site.register(Application)
