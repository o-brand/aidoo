from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from Golf.utils import create_date_string

def validate_dob(dobInput):

    min = datetime.strptime(create_date_string(100), '%Y-%m-%d').date()

    if min > dobInput:
        raise ValidationError(
            _('%(value)s is not a valid date'),
            params={'value': dobInput},
        )

    max = datetime.strptime(create_date_string(13), '%Y-%m-%d').date()

    if max < dobInput:
        raise ValidationError(
            _('%(value)s is not a valid date'),
            params={'value': dobInput},
        )



