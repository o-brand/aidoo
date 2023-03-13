from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import constraints, Q
from django.utils import timezone


def profile_id_rename(instance, filename): # pragma: no cover
    """Renames the image of the ID before uploading."""
    return "/".join(["ids", instance.username])

def profile_picture_rename(instance, filename): # pragma: no cover
    """Renames the profile picture before uploading."""
    return "/".join(["profilepics", instance.username])


class User(AbstractUser):
    """Extends new fields for the Django provided AbstractUser model."""

    # SCRIP
    # The actual available balance
    balance = models.IntegerField(default=24)

    # This balance is for jobs in progress
    # (the user has to pay the price of the post when they post it)
    frozen_balance = models.IntegerField(default=0)

    # EXTRA INFORMATION
    # Bio for the user. Displayed on the profile pages.
    biography = models.CharField(max_length=250, default="")

    # Date of birth, Null for charities
    date_of_birth = models.DateField(blank=True, null=True)
    
    # Used to keep track if the email is verified
    verified = models.BooleanField(default=False)

    # Used to give privilige to the user to be able to deal with reporting
    super_user = models.BooleanField(default=False)

    # Whether user is a charity or not
    charity = models.BooleanField(default=False)

    # NOTIFICATIONS
    # Recieve email notification when accepted or rejected from job
    opt_in_emails_application = models.BooleanField(default=True)

    # Recieve on site notification when accepted or rejected from job
    opt_in_site_application = models.BooleanField(default=True)

    # Recieve on site notification when a user applies for your job
    opt_in_site_applicant = models.BooleanField(default=True)

    # IMAGES
    # Used to store the profile picture
    profile_picture = models.ImageField(
        upload_to=profile_picture_rename, default="profilepics/default"
    )

    # Used to store the identity verification
    profile_id = models.ImageField(upload_to=profile_id_rename)

    # EXTRAS
    # Only used to create a superuser.
    REQUIRED_FIELDS = ["first_name", "last_name", "email", "date_of_birth"]

    class Meta:
        """This class creates a contraint for the model."""

        # Charities do no have date of birth but other users must have one
        constraints = [
            models.CheckConstraint(
                check=(Q(date_of_birth=None) & Q(charity=True))
                | (Q(charity=False) & ~Q(date_of_birth=None)),
                name="date_of_birth_for_charities",
            )
        ]



class Notification(models.Model):
    """This model represents notifications."""

    #Primary key
    notification_id = models.BigAutoField(primary_key=True)

    #Foreign Key to user who got the notification
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    #Short title summarizing the content of the notification
    title = models.CharField(max_length=50, default="Alert")

    #Content of the notification
    content = models.CharField(max_length=100)

    #Link to resolve the notification
    link = models.URLField(max_length=200)

    #Notification reviewed
    seen = models.BooleanField(default=False)

    # Time notificiation recorded
    time_of_notification = models.DateTimeField(default=timezone.now)
