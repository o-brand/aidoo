"""Aidoo URL Configuration"""

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),  # Admin pages (Django handles them)
    path("", include("login.urls")),  # Login pages + Welcome page
    path("jobs/", include("jobs.urls")),  # Jobs pages
    path("profile/", include("userprofile.urls")),  # Profile pages
    path("chat/", include("chat.urls")), # Chats pages
    path("store/", include("store.urls")), # Store pages
    path("superadmin/", include("superadmin.urls")), # Superadmin pages
    path("help/", include("help.urls")), # Help pages
    path("vendor/", include("vendor.urls")), # Redeem page
]
