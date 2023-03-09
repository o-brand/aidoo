from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from Golf.utils import create_date_string


def validate_deadline(dobInput):
    """Validates the deadline value."""

    # The min deadline is today.
    min = datetime.strptime(create_date_string(0), "%Y-%m-%d").date()
    if min > dobInput:
        raise ValidationError(
        # Throw an error.
            _("%(value)s is not a valid date. The minimum deadline is today."),
            params={"value": dobInput},
        )

    # The max deadline is one year ahead in the future.
    max = datetime.strptime(create_date_string(-1), "%Y-%m-%d").date()
    if max < dobInput:
        # Throw an error.
        raise ValidationError(
            _("%(value)s is not a valid date. The deadline cannot be more than 1 year from now."),
            params={"value": dobInput},
        )


def validate_hours(hours_input):
    """Validates the hours (between 1 and 8)."""

    # The number of hours is not between 1 and 8 or not integer.
    if hours_input < 0 or hours_input > 8 or hours_input % 1 != 0:
        # Throw an error.
        raise ValidationError(
            "The number of hours is not valid.",
        )


def validate_half_hours(half_hours_input):
    """Validates the minutes (0 or 30)."""

    # The number of minutes is not 0 and not 30.
    if half_hours_input != 0 and half_hours_input != 30:
        # Throw an error.
        raise ValidationError(
            "The number of minutes is not valid. Only 0 and 30 minutes are allowed.",
        )
