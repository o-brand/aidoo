from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db.models import constraints
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    """Extends new fields for the Django provided AbstractUser model."""

    balance = models.IntegerField(default=24)
    date_of_birth = models.DateField()
    rating = models.FloatField(default=0)
    # Recieve email notification when accepted or rejected from job
    opt_in_emails_application = models.BooleanField(default=True)
    # Recieve on site notification when accepted or rejected from job
    opt_in_site_application = models.BooleanField(default=True)
    # Recieve on site notification when a user applies for your job
    opt_in_site_applicant = models.BooleanField(default=True)
    biography = models.CharField(max_length=250, default="")
    frozen_balance = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)
    # Used to store the profile picture    
    profile_picture = models.ImageField(upload_to='profilepics/', default='profilepics/default.png')
    # Used to store the identity verification
    profile_id = models.ImageField(upload_to='ids/', default='ids/empty.png')
    # Only used to create a superuser.
    REQUIRED_FIELDS = ["first_name", "last_name", "email", "date_of_birth"]
    

class Notification(models.Model):
    """This model represents notifications."""

    #Primary key
    notification_id = models.BigAutoField(primary_key=True)

    #Foreign Key to user who got the notification
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    #Content of the notification
    content = models.CharField(max_length=100)

    #Link to resolve the notification
    link = models.URLField(max_length=200)

    #Notification reviewed
    seen = models.BooleanField(default=False)
