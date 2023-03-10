from django.shortcuts import render
from cryptography.fernet import Fernet
import base64
from django.conf import settings
from django.http import Http404
from store.models import Sale


def redeem(request, token):
    # Render the page

    try:
        fact = base64.urlsafe_b64decode(token)
        cipher_suite = Fernet(settings.KEY)
        fact = cipher_suite.decrypt(fact).decode("ascii")

        sale, _ = fact.split("#")
        item = Sale.objects.get(pk=sale).purchase
    except Exception:
        raise Http404()
        
    context = {
        "vendor" :"true",
        "item": item,
        
    }
    return render(request, "vendor/index.html", context)

def redeem_call(request):
    pass
