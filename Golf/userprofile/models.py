from django.db import models
from django.contrib.auth.models import User

class UserExtended(models.Model):
    user_id = models.OneToOneField(
        User,
        on_delete = models.CASCADE,
        primary_key = True
    )
    balance = models.IntegerField(default=0)
    date_of_birth = models.DateField()
    rating = models.FloatField(default=0)