from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.contrib.auth import get_user_model
from chat.models import Room # Move to admin models when created


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


# # Currently not migrated, should be in the models of the admin app
# class Report(models.Model):
#     """This model is used to represent a report filed against a job or user"""

#     class ReportType(models.TextChoices):
#         """This class stores the available values for the report type."""
#         PROFILE = 'Profile', ('Profile')
#         COMMENT = 'Comment', ('Comment')
#         JOB = 'Job', ('Job')
#         CHAT = 'Chat', ('Chat')

#     class ReportStatus(models.TextChoices):
#         """This class stores the available values for the status."""
#         OPEN = 'Open', ('Open')
#         TICKETED = 'Ticketed', ('Ticketed')
#         RESOLVED = 'Resolved', ('Resolved')
    
#     # Primary key
#     report_id = models.BigAutoField(primary_key=True)
    
#     # ID of reported job, if the report concerns a job post
#     reported_job = models.ForeignKey(Job,
#         on_delete=models.CASCADE,
#         default=None)
    
#     # ID of reported job, if the report concerns a chat
#     reported_room = models.ForeignKey(Room, 
#         on_delete=models.CASCADE,
#         default=None)
    
#     # User being reported
#     reported_user = models.ForeignKey(User,
#         related_name="reported",
#         on_delete=models.CASCADE)
    
#     # User filing the report
#     reporting_user = models.ForeignKey(User,
#         related_name="reporting", 
#         on_delete=models.CASCADE)
    
#     # Content of the complaint, should take an adequate min length
#     complaint = models.CharField(max_length=1000)
    
#     # The time at which the report was first filed
#     reporting_time = models.DateTimeField(default=timezone.now)
   
#    # The time at which the report last changed status
#     last_update_time = models.DateTimeField(default=None)
    
#     # The status of dealing with the report
#     status = models.CharField(choices=ReportStatus.choices, max_length=10)
    
#     # The type of report
#     type = models.CharField(choices=ReportType.choices, max_length=10)


# # Should be in the models of the admin app
# class ReportTicket(models.Model):
#     pass


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
