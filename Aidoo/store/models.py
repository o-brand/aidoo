from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.db import models
from django.utils import timezone


# Get actual user model.
User = get_user_model()


def item_picture_rename(instance, filename): # pragma: no cover
    """Renames the image before uploading."""
    return "/".join(
        ["storeitem", instance.item_name.replace(" ", "-").lower()]
    )


class Item(models.Model):
    """This model is used to represent an item for sale in the shop."""

    # Primary key
    item_id = models.BigAutoField(primary_key=True)

    # Name of item
    item_name = models.CharField(max_length=100)

    # Brief description of the item
    description = models.CharField(max_length=250)

    # Price of the item
    price = models.IntegerField()

    # Current amount of the item left in stock
    stock = models.IntegerField()

    # True if the item is on offer (i.e. displaying) in the shop
    on_offer = models.BooleanField()

    # The maximum amount of this item that a user can buy
    limit_per_user = models.IntegerField(blank=True, default=None, null=True)

    # image field
    item_picture = models.ImageField(upload_to=item_picture_rename)


class Sale(models.Model):
    """This model is used to represent the sale of an item in the shop, where
    each item sold is recorded separately"""

    # Primary key
    sale_id = models.BigAutoField(primary_key=True)

    # Foreign key to the Item table for the item purchased from the store
    purchase = models.ForeignKey(Item, on_delete=models.CASCADE)

    # Foreign key to User who bought the item
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)

    # Amount of the item purchased
    quantity = models.IntegerField()

    # Whether item is redeemed
    redeemed = models.BooleanField(default=False)

    # The time at which the sale was recorded
    time_of_sale = models.DateTimeField(default=timezone.now)


class Transfer(models.Model):
    """This model is used to represent the transfer of coins from one user to
    another"""

    # Primary key
    transfer_id = models.BigAutoField(primary_key=True)

    # Foreign key to User giving the money
    sender = models.ForeignKey(
        User, related_name="sender", on_delete=models.CASCADE
    )

    # Foreign key to User receiving the money
    recipient = models.ForeignKey(
        User, related_name="recipient", on_delete=models.CASCADE
    )

    # Amount of money being transferred
    amount = models.IntegerField()

    # Message to send to the beneficiary
    note = models.CharField(max_length=250, default="")

    # The time at which the trasfer was recorded
    time_of_transfer = models.DateTimeField(default=timezone.now)


class Moderation(models.Model):
    """Overarching model for the site"""

    # Tied up to a django site
    site = models.OneToOneField(Site, on_delete=models.CASCADE, primary_key=True)

    # Holds all points spent in the store
    bank = models.IntegerField(default=0)

    # Money to be paid per ticket
    ticket_payout = models.IntegerField(default=2)

    # Holds all points due to be paid for guardians
    frozen_bank = models.IntegerField(default=0)

    # Decides if chat deletion is active or not for reporting
    chat_deletion = models.BooleanField(default=True)
