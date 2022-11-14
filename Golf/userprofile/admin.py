from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

# Extended Admin, just for us.
class UserAdmin(BaseUserAdmin):

    # The fields to be used in displaying the User model.
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "date_of_birth")}),
        (_("Extra info"), {"fields": ("rating", "balance")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
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
