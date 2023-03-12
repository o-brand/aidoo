from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


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
