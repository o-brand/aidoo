from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.contrib.auth import get_user_model


# Get actual user model.
User = get_user_model()


class Job(models.Model):
    """This model is used to represent a job."""

    # Primary key
    job_id = models.BigAutoField(primary_key=True)

    # Foreign key to the User model (user who posted it)
    poster_id = models.ForeignKey(User, on_delete=models.CASCADE)

    # Location of the job
    location = models.CharField(max_length=8)

    # Title of the job
    job_title = models.CharField(max_length=50)

    # Short description. It is displayed in the list.
    job_short_description = models.CharField(max_length=50)

    # Long description. It is displayed in the details page.
    job_description = models.CharField(max_length=1000)

    # The time of posting (it has default value)
    posting_time = models.DateTimeField(default=timezone.now)

    # The points for the job (must be at least 1)
    points = models.IntegerField(validators=[MinValueValidator(1)])

    # The deadline, it is optional
    deadline = models.DateField(default=None, blank=True, null=True)

    # We can hide the job later
    hidden = models.BooleanField(default=False)

    # If the poster already accepted somebody, then this is True
    assigned = models.BooleanField(default=False)

    # If the poster marked this job as completed, then this is True
    completed = models.BooleanField(default=False)

#
class Report(models.Model):
    """This model is used to represent a form to submit report"""

    #Field to describe the issue
    description  = models.CharField(max_length=1000)
#

class Bookmark(models.Model):
    """This model is used to represent a bookmark for the user."""

    # Primary key
    bookmark_id = models.BigAutoField(primary_key=True)

    # Foreign key to the User model (user who bookmarked the job)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    # Foreign key to the Job model (the job which is bookmarked now)
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)

    # The time of bookmarking (it has default value)
    saving_time = models.DateTimeField(default=timezone.now)

    class Meta:
        """This class creates a contraint for the model."""

        # Prevent a user to save a job twice
        constraints = [
            models.UniqueConstraint(
                fields=["user_id", "job_id"], name="bookmark_user_job_combo"
            )
        ]


class Application(models.Model):
    """This model is used to represent an application for a job by a user."""

    class JobStatus(models.TextChoices):
        """This class stores the available values for the progress."""
        APPLIED = 'AP', ('Applied') # User applied
        REJECTED = 'RE', ('Rejected') # Poster rejected the user
        ACCEPTED = 'AC', ('Accepted') # Poster accepted the job
        WITHDRAWN = 'WD', ('Withdrawn') # Applicant withdrew from the job
        DONE = 'DN', ('Done') # Job has been finished
        CONFLICT = 'CO', ('Conflict') # Conflict in releasing points

    # Primary key
    application_id = models.BigAutoField(primary_key=True)

    # Foreign key to the User model (user who clicked on "apply")
    applicant_id = models.ForeignKey(User, on_delete=models.CASCADE)

    # Foreign key to the Job model (the job which is this application about)
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE)

    # Describes progress of the application process
    status = models.CharField(
        max_length=2,
        choices=JobStatus.choices,
        default=JobStatus.APPLIED,
    )

    # The time of applying
    time_of_application = models.DateTimeField(default=timezone.now)

    # The time of final status (WITHDRAWN, DONE)
    time_of_final_status = models.DateTimeField(default=None, blank=True, null=True)


    class Meta:
        """This class creates a contraint for the model."""

        # Prevent a user to apply for a job twice
        constraints = [
            models.UniqueConstraint(
                fields=['applicant_id', 'job_id'], name='application_user_job_combo'
            )
        ]
