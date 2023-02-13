from django.contrib import admin
from .models import Job, Bookmark, Application, Report


# Enable editing these models via /admin/.
admin.site.register(Job)
admin.site.register(Bookmark)
admin.site.register(Application)
admin.site.register(Report)
