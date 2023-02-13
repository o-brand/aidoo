from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import Item, Sale

User = get_user_model()

def home(request):
    # Render the main shop page
    actual_user_id = request.user.id

    try:
        _ = User.objects.get(pk=actual_user_id)
    except User.DoesNotExist:
        # This should not happen.
        raise Http404("User does not exist.")

    items = Item.objects.filter(on_offer=True)
    purchases = Sale.objects.filter(buyer=request.user)
    purchased_items = [x.purchase for x in purchases]

    context = {
        "items": items,
        "purchases": purchased_items
    }
    return render(request, "store/storefront.html", context)

def buyitem_call(request):
    """User buys an item from the store"""
    if request.method == "POST":
        # Get the item ID or -1 if it is not found
        item_id = request.POST.get("item_id", -1)
        user = request.user

        # Check if the item ID is valid
        items = Item.objects.filter(pk=item_id)
        item_id_exists = len(items) == 1
        if not item_id_exists:
            raise Http404()
        item = items[0]

        if not item.on_offer:
            raise Http404()

        # Get buyer
        buyer = User.objects.get(id=user.id)

        # Get quantity
        try:
            quantity = int(request.POST.get("quantity", -1))
        except ValueError:
            raise Http404()
        if quantity <= 0:
            raise Http404() # Not sure if this is the right error code

        # Create new sale instance
        sale = Sale.objects.create(
            purchase = item,
            buyer = buyer,
            quantity = quantity
        )

        # Work...
        # We def need to do a validation of sufficient funds on the frontend,
        # but should we also do it here? If so, also for job post/job done?
        # Deduct points from buyer
        buyer.balance = buyer.balance - item.price * sale.quantity
        # Reduce the stock of the item by the sale qty
        item.stock = item.stock - sale.quantity

        item.save()
        buyer.save()
        sale.save()

        return render(request, "htmx/buy-item-bought.html")

    # If it is not POST
    raise Http404()