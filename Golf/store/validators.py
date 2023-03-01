from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


# Get actual user model.
User = get_user_model()


def validate_recipient(username):
    """Validates the recipient value."""

    if len(User.objects.filter(username=username)) != 1:
        raise ValidationError(
        # Throw an error.
            _("There is no user with the username %(value)s."),
            params={"value": username},
        )

def validate_transfer_budget(amount):
    pass
