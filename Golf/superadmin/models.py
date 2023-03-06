from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from jobs.models import Job
from chat.models import Room


# Get actual user model.
User = get_user_model()


class Report(models.Model):
    """This model is used to represent a report filed against a job or user"""

    class ReportType(models.TextChoices):
        """This class stores the available values for the report type."""
        PROFILE = 'Profile', ('Profile')
        COMMENT = 'Comment', ('Comment')
        JOB = 'Job', ('Job')
        CHAT = 'Chat', ('Chat')

    class ReportStatus(models.TextChoices):
        """This class stores the available values for the status."""
        OPEN = 'Open', ('Open')
        TICKETED = 'Ticketed', ('Ticketed')
        RESOLVED = 'Resolved', ('Resolved')

    # ID of reported job, if the report concerns a job post
    reported_job = models.ForeignKey(Job,
        on_delete=models.CASCADE,
        default=None)
    
    # ID of reported job, if the report concerns a chat
    # Fix and uncomment when 
    # reported_room = models.ForeignKey(Room, 
    #     on_delete=models.CASCADE,
    #     default=None)

    # ID of reported comment, if the report concerns a comment
    # To be implemented alongside user comments
    
    # User being reported
    reported_user = models.ForeignKey(User,
        related_name="reported",
        on_delete=models.CASCADE)
    
    # User filing the report
    reporting_user = models.ForeignKey(User,
        related_name="reporting", 
        on_delete=models.CASCADE)
    
    # Content of the complaint, should take an adequate min length
    complaint = models.CharField(max_length=1000)
    
    # The time at which the report was first filed
    reporting_time = models.DateTimeField(default=timezone.now)
   
   # The time at which the report last changed status
    last_update_time = models.DateTimeField(blank=True, 
        default=None, 
        null=True)
    
    # The status of dealing with the report
    status = models.CharField(
        choices=ReportStatus.choices, 
        max_length=10, 
        default=ReportStatus.OPEN
    )
    
    # The type of report
    type = models.CharField(choices=ReportType.choices, max_length=10)


#Model for assigining reports to reviewers
class ReportTicket(models.Model):

    #primary key
    ticket_id = models.BigAutoField(primary_key=True), 

    #id of the reported object
    report_id  = models.ForeignKey(Report, on_delete=models.CASCADE, default=None), 

    #id of a user assigned to resolve the issue
    user_id = models.ForeignKey(User, on_delete=models.CASCADE),

    #the result of the resolutiom
    answer=models.BooleanField(default=False),

    #time stamp for assigning the job
    time_assigned = models.DateTimeField(default=timezone.now),

    #time stamp for resolving the report
    time_resolved = models.DateTimeField(default=None, blank=True, null=True), 

    
class ConflictResolution(models.Model):
    class ConflictType(models.TextChoices):
         """available values for the conflict type"""
         #FINISH
         CONFLICT1 = 'Conflict1', ('Conflict1')
         CONFLICT2 = 'Conflict2', ('Conflict2')
    
    class ConflictStatus(models.TextChoices):
        "available values for the conflict status"

        OPEN = 'Open', ('Open')
        FLAGGED = 'Flagged', ('Flagged')
        RESOLVED = 'Resolved', ('Reesolved')

    #Primary key
    conflict_id = models.BigAutoField(primary_key=True)

    #conflicted_action
    job_id = models.ForeignKey(Job, 
        on_delete = models.CASCADE, 
        default=None)
    user1_id = models.ForeignKey(User,
        related_name = "user1",
        on_delete=models.CASCADE)
    
    #IF 2 USERS ARE INVOLVED
    #user2_id = models.ForeignKey(User,
        #related_name = "user2",
        #on_delete=models.CASCADE)

    #reason for the conflict
    content = models.CharField(max_length=100)

    #time the conflict was issues
    conflict_time = models.DateTimeField(default=timezone.now)

    #the last update time
    conflict_update_time = models.DateTimeField(blank=True, 
        default=None, 
        null=True)
    
    #status of dealing with the conflict
    status = models.CharField(
        choices=ConflictStatus.choices, 
        max_length=10,
        default=ConflictStatus.OPEN
    )

    #type of conflict
    type = models.CharField(
        choices=ConflictType.choices,
        max_length=10
    )
