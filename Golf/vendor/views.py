from django.shortcuts import render
from cryptography.fernet import Fernet
import base64
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import Http404
from store.models import Sale


# Get actual user model.
User = get_user_model()


def redeem(request, token):
    """Displays a bought item to be redeemed."""

    try:
        fact = base64.urlsafe_b64decode(token)
        cipher_suite = Fernet(settings.KEY)
        fact = cipher_suite.decrypt(fact).decode("ascii")

        sale, buyer = fact.split("#")
        sale = Sale.objects.get(pk=sale)
        buyer = User.objects.get(pk=buyer)

        if sale.buyer != buyer:
            raise Http404()

        item = sale.purchase

    except Exception:
        raise Http404()

    context = {
        "vendor" :"true",
        "redeemed": sale.redeemed,
        "item": item,
        "sale": sale.pk,
        "buyer": buyer.pk,
    }
    return render(request, "vendor/index.html", context)


def redeem_call(request):
    """Redeem a bought item."""
    if request.method == "POST":
        # Get the sale ID or -1 if it is not found
        sale_id = request.POST.get("sale", -1)

        # Get the user ID or -1 if it is not found
        buyer_id = request.POST.get("buyer", -1)

        # Check if the sale ID is valid
        sales = Sale.objects.filter(sale_id=sale_id)
        sale_id_exists = len(sales) == 1
        if not sale_id_exists:
            raise Http404()
        sale = sales[0]

        # Check if the user ID is valid
        buyers = User.objects.filter(id=buyer_id)
        buyer_id_exists = len(buyers) == 1
        if not buyer_id_exists:
            raise Http404()
        buyer = buyers[0]

        # Check if the buyer is the actual buyer
        if sale.buyer != buyer:
            raise Http404()

        # Redeem the item
        # If the item was redeemed before, then nothing happens now.
        sale.redeemed = True
        sale.save()

        return render(request, "vendor/redeemed.html")

    # If it is not POST
    raise Http404()
