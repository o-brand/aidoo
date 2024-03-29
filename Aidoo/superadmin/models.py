from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from jobs.models import Job
from chat.models import Room


# Get actual user model.
User = get_user_model()


class Report(models.Model):
    """This model is used to represent a report filed against a job or user"""

    class ReportType(models.TextChoices):
        """This class stores the available values for the report type."""

        PROFILE = "Profile", ("Profile")
        COMMENT = "Comment", ("Comment")
        JOB = "Job", ("Job")
        CHAT = "Chat", ("Chat")

    class ReportStatus(models.TextChoices):
        """This class stores the available values for the status."""

        OPEN = "Open", ("Open")
        TICKETED = "Ticketed", ("Ticketed")
        RESOLVED = "Resolved", ("Resolved")

    class ReportResult(models.TextChoices):
        """This class stores the possible outcomes of a result"""

        BAN = "BA", ("Ban")
        NOT_BAN = "NB", ("Not_Ban")

    # Primary key
    report_id = models.BigAutoField(primary_key=True)

    # ID of reported job, if the report concerns a job post
    reported_job = models.ForeignKey(Job, on_delete=models.CASCADE)

    # User being reported
    reported_user = models.ForeignKey(
        User, related_name="reported", on_delete=models.CASCADE
    )

    # User filing the report
    reporting_user = models.ForeignKey(
        User, related_name="reporting", on_delete=models.CASCADE
    )

    # Content of the complaint, should take an adequate min length
    complaint = models.CharField(max_length=1000)

    # The time at which the report was first filed
    reporting_time = models.DateTimeField(default=timezone.now)

    # The time at which the report last changed status
    last_update_time = models.DateTimeField(blank=True, default=timezone.now)

    # The status of dealing with the report
    status = models.CharField(
        choices=ReportStatus.choices, max_length=10, default=ReportStatus.OPEN
    )

    # The type of report
    type = models.CharField(choices=ReportType.choices, max_length=10)

    # Outcome of the report
    answer = models.CharField(
        choices=ReportResult.choices, blank=True, null=True, default=None, max_length=2
    )


class ReportTicket(models.Model):
    """This model is used to assigining reports to reviewers"""

    class TicketStatus(models.TextChoices):
        """This class stores the available values for the status."""

        OPEN = "OP", ("Open")
        RESOLVED = "RE", ("Resolved")

    class TicketResult(models.TextChoices):
        """This class stores the possible outcomes of a result"""

        BAN = "BA", ("Ban")
        NOT_BAN = "NB", ("Not_Ban")

    # Primary key
    ticket_id = models.BigAutoField(primary_key=True)

    # Id of the reported object
    report_id = models.ForeignKey(Report, on_delete=models.CASCADE)

    # Id of a user assigned to resolve the issue
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    # The result of the resolutiom
    answer = models.CharField(
        choices=TicketResult.choices, blank=True, null=True, default=None, max_length=2
    )

    # Time stamp for assigning the job
    time_assigned = models.DateTimeField(default=timezone.now)

    # Status of the ticket
    status = models.CharField(
        choices=TicketStatus.choices, default=TicketStatus.OPEN, max_length=2
    )


class ConflictResolution(models.Model):
    """This model is used for dealing with conflict resolution, in progress"""

    class ConflictType(models.TextChoices):
        """available values for the conflict type"""

        CONFLICT1 = "Conflict1", ("Conflict1")
        CONFLICT2 = "Conflict2", ("Conflict2")

    class ConflictStatus(models.TextChoices):
        "available values for the conflict status"

        OPEN = "Open", ("Open")
        FLAGGED = "Flagged", ("Flagged")
        RESOLVED = "Resolved", ("Reesolved")

    # Primary key
    conflict_id = models.BigAutoField(primary_key=True)

    # Conflicted action
    job_id = models.ForeignKey(Job, on_delete=models.CASCADE, default=None)
    user1_id = models.ForeignKey(User, related_name="user1", on_delete=models.CASCADE)

    # Reason for the conflict
    content = models.CharField(max_length=100)

    # Time the conflict was issues
    conflict_time = models.DateTimeField(default=timezone.now)

    # The last update time
    conflict_update_time = models.DateTimeField(blank=True, default=None, null=True)

    # Status of dealing with the conflict
    status = models.CharField(
        choices=ConflictStatus.choices, max_length=10, default=ConflictStatus.OPEN
    )

    # Type of conflict
    type = models.CharField(choices=ConflictType.choices, max_length=10)
