from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Notification


class UserAdmin(BaseUserAdmin):
    """Extended Admin, just for developers. To create a view of data in the /admin/ page."""

    # The fields to be used in displaying the User model.
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "date_of_birth", "biography")}),
        (_("Account Settings info"), 
            {"fields": ("opt_in_emails_application", 
                        "opt_in_site_application", 
                        "opt_in_site_applicant")}),
        (_("Extra info"), {"fields": ("rating", "balance", "frozen_balance")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "verified",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    # Attributes to create a new user.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "date_of_birth", "password1", "password2"),
            },
        ),
    )


# Register the new User and UserAdmin.
admin.site.register(User, UserAdmin)
admin.site.register(Notification)
