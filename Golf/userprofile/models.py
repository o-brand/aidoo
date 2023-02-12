from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Extends new fields for the Django provided AbstractUser model."""

    balance = models.IntegerField(default=0)
    date_of_birth = models.DateField()
    rating = models.FloatField(default=0)
    opt_in_emails = models.BooleanField(default=True)

    # Only used to create a superuser.
    REQUIRED_FIELDS = ["first_name", "last_name", "email", "date_of_birth"]

