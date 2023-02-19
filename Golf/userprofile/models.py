from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


class User(AbstractUser):
    """Extends new fields for the Django provided AbstractUser model."""

    balance = models.IntegerField(default=0)
    date_of_birth = models.DateField()
    rating = models.FloatField(default=0)
    opt_in_emails = models.BooleanField(default=True)
    biography = models.CharField(max_length=250, default="")
    frozen_balance = models.IntegerField(default=0)

    # Only used to create a superuser.
    REQUIRED_FIELDS = ["first_name", "last_name", "email", "date_of_birth"]
    
class Notifications(models.Model):
    """This model represents notifications."""

    #Primary key
    notification_id = models.BigAutoField(primary_key=True)

    #Foreign Key to user who got the notification
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    #Content of the notification
    content = models.CharField(max_length=100)

    #Link to resolve the notification
    link = models.CharField(max_length=50)

    #Notification reviewed
    seen = models.BooleanField(default=False) 
