from django.db import models

class JobPosting(models.Model):
    job_id = models.BigAutoField(primary_key=True)
    poster_id = models.ForeignKey('Poster ID', on_delete=models.CASCADE,)
    job_title = models.CharField(max_length=50)
    job_description = models.CharField(max_length=300)
    posting_time = models.DateTimeField()
    points = models.IntegerField() #can we make sure it's positive?
    category = models.CharField(max_length=50)
    assigned = models.BooleanField()
    completed = models.BooleanField()