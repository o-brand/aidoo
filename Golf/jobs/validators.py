from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from Golf.utils import create_date_string

def validate_deadline(dobInput):

    min = datetime.strptime(create_date_string(0), '%Y-%m-%d').date()

    if min > dobInput:
        raise ValidationError(
            _('%(value)s is not a valid date. The minimum deadline is today.'),
            params={'value': dobInput},
        )

    max = datetime.strptime(create_date_string(-1), '%Y-%m-%d').date()

    if max < dobInput:
        raise ValidationError(
            _('%(value)s is not a valid date. The deadline cannot be more than 1 year from now.'),
            params={'value': dobInput},
        )
