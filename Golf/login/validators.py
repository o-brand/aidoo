from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from Golf.utils import create_date_string


def validate_dob(dobInput):
    """Validates the date of birth value."""

    # The max age is 100 years.
    min = datetime.strptime(create_date_string(100), "%Y-%m-%d").date()
    if min > dobInput:
        # Throw an error.
        raise ValidationError(
            _("%(value)s is not a valid date. You are too old for this platform."),
            params={"value": dobInput},
        )

    # The min age is 13 years.
    max = datetime.strptime(create_date_string(13), "%Y-%m-%d").date()
    if max < dobInput:
        # Throw an error.
        raise ValidationError(
            _("%(value)s is not a valid date. You are too young for this platform."),
            params={"value": dobInput},
        )
