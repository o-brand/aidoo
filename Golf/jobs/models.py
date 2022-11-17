from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model() # Get user model

class Job(models.Model):
    job_id = models.BigAutoField(primary_key=True)
    poster_id = models.ForeignKey(User, on_delete=models.CASCADE) # Should we use something else on delete?
        #making the change general and it happens everywhere, if you delete user, everything about the user is deleted
    location = models.CharField(max_length=8)
    job_title = models.CharField(max_length=50)
    job_short_description = models.CharField(max_length=50)
    job_description = models.CharField(max_length=1000)
    posting_time = models.DateTimeField(default=timezone.now)
    points = models.IntegerField(validators=[MinValueValidator(1)])
    deadline = models.DateField(default=None, blank=True, null=True)
    hidden = models.BooleanField(default=False)
    assigned = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)


class Bookmark(models.Model):
    bookmark_id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE) # User who bookmarked job
    job_id = models.ForeignKey(Job, on_delete = models.CASCADE)
    saving_time = models.DateTimeField()

    class Meta:
         constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'job_id'], name='bookmark_user_job_combo'
            )
        ]


#a table
class Application(models.Model):
    class JobStatus(models.TextChoices):
        #attributes for the status of the of the button
        APPLIED = 'AP', ('Applied')
        REJECTED = 'RE', ('Rejected')
        ACCEPTED = 'AC', ('Accepted')
        WITHDRAWN = 'WD', ('Withdrawn') # Applicant withdrew from job
        DONE = 'DN', ('Done') # Job has been finished
        CONFLICT = 'CO', ('Conflict') # Conflict in releasing points

    #primary key
    application_id = models.BigAutoField(primary_key=True)
    #foreign key - back to the User table, user_id of the applicant
    applicant_id = models.ForeignKey(User, on_delete = models.CASCADE)
    job_id = models.ForeignKey(Job, on_delete = models.CASCADE)
    #describes progess of the Apply process
    status = models.CharField(
        max_length=2,
        choices=JobStatus.choices,
        default=JobStatus.APPLIED,
    )
    time_of_application = models.DateTimeField(default=timezone.now)
    time_of_final_status = models.DateTimeField(default=None, blank=True, null=True)


    #this helps Django and constraints that ids are unique
    class Meta:
         constraints = [
            models.UniqueConstraint(
                fields=['applicant_id', 'job_id'], name='application_user_job_combo'
            )
        ]
#kay, i need this explained