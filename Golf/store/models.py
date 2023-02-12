from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

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

class Sale(models.Model):
    """This model is used to represent the sale of an item in the shop,
    where each item sold is recorded separately"""

    # Primary key
    sale_id = models.BigAutoField(primary_key=True)

    # Foreign key to the Item table for the item purchased from the store
    purchase = models.ForeignKey(Item, on_delete=models.CASCADE)

    # Foreign key to User who bought the item
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)

    # Amount of the item purchased
    quantity = models.IntegerField(default=1) #Take out default later

    # The time at which the sale was recorded
    time_of_sale = models.DateTimeField(default=timezone.now)


