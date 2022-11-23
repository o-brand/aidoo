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
