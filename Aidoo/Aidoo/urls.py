"""Aidoo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
