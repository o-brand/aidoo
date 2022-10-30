from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class JobPosting(models.Model):
    job_id = models.BigAutoField(primary_key=True)
    poster_id = models.ForeignKey(User, on_delete=models.CASCADE) # Should we use something else on delete?
    location = models.CharField(max_length=8)
    job_title = models.CharField(max_length=50)
    job_short_description = models.CharField(max_length=50)
    job_description = models.CharField(max_length=1000)
    posting_time = models.DateTimeField()
    points = models.IntegerField(validators=[MinValueValidator(1)])
    assigned = models.BooleanField()
    completed = models.BooleanField()

class UserExtended(models.Model):
    user_id = models.OneToOneField(
        User,
        on_delete = models.CASCADE,
        primary_key = True
    )
    balance = models.IntegerField()
    date_of_birth = models.DateField()
    rating = models.FloatField()

class UserSaveForLater(models.Model):
    save_for_later_id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    job_id = models.ForeignKey(JobPosting, on_delete = models.CASCADE)
    saving_time = models.DateTimeField()

    class Meta:
         constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'job_id'], name='sfl_user_job_combo'
            )
        ]

class JobProcess(models.Model):
    class JobStatus(models.TextChoices):
        APPLIED = 'AP', ('Applied')
        REJECTED = 'RE', ('Rejected')
        ACCEPTED = 'AC', ('Accepted')

    job_process_id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    job_id = models.ForeignKey(JobPosting, on_delete = models.CASCADE)
    status = models.CharField(
        max_length=2,
        choices=JobStatus.choices,
        default=JobStatus.APPLIED,
    )

    class Meta:
         constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'job_id'], name='process_user_job_combo'
            )
        ]
