from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


# Get actual user model.
User = get_user_model()


class Room(models.Model):
    """This model is used to represent a room where two user can chat."""

    # Primary key
    room_id = models.BigAutoField(primary_key=True)

    # Foreign key to the User model (user who created the room)
    user_1 = models.ForeignKey(User, related_name= "inviter", on_delete=models.CASCADE)

    # Foreign key to the User model (the other user)
    user_2 = models.ForeignKey(User, related_name= "invitee", on_delete=models.CASCADE)

    # The time of creation (it has default value)
    creation_time = models.DateTimeField(default=timezone.now)

    class Meta:
        """This class creates a contraint for the model."""

        # Prevent a user to have two rooms with somebody
        constraints = [
            models.UniqueConstraint(
                fields=["user_1", "user_2"], name="user_user_combo"
            )
        ]


class Message(models.Model):
    """This model is used to store a message for a room."""

    # Primary key
    message_id = models.BigAutoField(primary_key=True)

    # The room which the message belongs to
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)

    # The user who sent the message
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    # The content of the message
    content = models.TextField()

    # The time the message was sent
    date_time = models.DateTimeField(default=timezone.now)

    class Meta:
        """This class specifies the order for the model."""

        # Ordering
        ordering = ('date_time',)
