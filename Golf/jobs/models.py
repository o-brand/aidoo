from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone

class JobPosting(models.Model):
    job_id = models.BigAutoField(primary_key=True)
    poster_id = models.ForeignKey(User, on_delete=models.CASCADE) # Should we use something else on delete?
    location = models.CharField(max_length=8)
    job_title = models.CharField(max_length=50)
    job_short_description = models.CharField(max_length=50)
    job_description = models.CharField(max_length=1000)
    posting_time = models.DateTimeField(default=timezone.now)
    points = models.IntegerField(validators=[MinValueValidator(1)])
    deadline = models.DateTimeField(default=None, blank=True, null=True)
    hidden = models.BooleanField(default=False)
    assigned = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    @staticmethod
    def has_been_saved():
        print([u.job_id for u in UserSaveForLater.objects.select_related('job_id')])
        return UserSaveForLater.objects.select_related('job_id')
    

class UserExtended(models.Model):
    user_id = models.OneToOneField(
        User,
        on_delete = models.CASCADE,
        primary_key = True
    )
    balance = models.IntegerField(default=0)
    date_of_birth = models.DateField()
    rating = models.FloatField(default=0)

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
