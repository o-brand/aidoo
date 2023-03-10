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
    # Render the page

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

    except Exception: # Should we use a more specific kind of exception?
        raise Http404()
        
    context = {
        "vendor" :"true",
        "item": item,
    }
    return render(request, "vendor/index.html", context)

def redeem_call(request):
    pass
