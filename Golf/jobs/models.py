from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class JobPosting(models.Model):
    job_id = models.BigAutoField(primary_key=True)
    location = models.CharField(max_length=8)
    poster_id = models.ForeignKey(User, on_delete=models.CASCADE) # Should we use something else on delete?
    job_title = models.CharField(max_length=50)
    job_short_description = models.CharField(max_length=50)
    job_description = models.CharField(max_length=1000)
    posting_time = models.DateTimeField()
    points = models.IntegerField(validators=[MinValueValidator(1)])
    assigned = models.BooleanField()
    completed = models.BooleanField()
