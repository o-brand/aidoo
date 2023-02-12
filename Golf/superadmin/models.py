# from django.db import models
# from django.utils import timezone
# from django.contrib.auth import get_user_model
# from jobs.models import Job
# # from chat.models import Room # Activate when chats finalized

# # Get actual user model.
# User = get_user_model()

# # Currently not migrated
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
#     # Fix and uncomment when 
#     # reported_room = models.ForeignKey(Room, 
#     #     on_delete=models.CASCADE,
#     #     default=None)

#     # ID of reported comment, if the report concerns a comment
#     # To be implemented alongside user comments
    
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


# # Model for assigining reports to reviewers
# # class ReportTicket(models.Model):
# #     pass