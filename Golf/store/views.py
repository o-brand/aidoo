import base64
import math
import mimetypes
import qrcode
from cryptography.fernet import Fernet
from email.mime.image import MIMEImage
from io import BytesIO
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from userprofile.models import Notification
from .forms import TransferForm, BuyForm
from .models import Item, Sale, Transfer


# Get actual user model.
User = get_user_model()


def calculate_choices(me, item, purchases):
    # Limit per user - already bought OR the stock
    if item.limit_per_user is not None:
        can_buy_below_limit = item.limit_per_user - sum(
            [x.quantity for x in purchases]
        )
    else:
        can_buy_below_limit = item.stock

    # The maximal quantity that can be bought using the balance
    can_afford = me.balance // item.price

    # Takes the minimum of the (limit per user - already bought OR the stock),
    # the stock, the display limit of 5, and the maximal quantity that can be bought using the balance
    return range(
        1,
        min(can_buy_below_limit, item.stock, 5, can_afford) + 1,
    )


def home(request):
    """Render the main shop page"""
    me = request.user
    items = Item.objects.filter(on_offer=True)
    purchases = Sale.objects.filter(buyer=me)
    purchased_items = [x.purchase for x in purchases]

    forms = dict()
    for item in items:
        # Calculate the available choices
        values = calculate_choices(me, item, purchases.filter(purchase=item))

        if len(values) > 0:
            forms[item] = BuyForm(values)
        else:
            forms[item] = False

    context = {
        "items": items,
        "purchases": purchased_items,
        "forms": forms,
    }
    return render(request, "store/index.html", context)


def buyitem_call(request):
    """Buy an item and return back the new form."""
    if request.method == 'POST':
        buyer = request.user

        # Get the item ID or -1 if it is not found
        item_id = request.POST.get("purchase", -1)

        # Check if the item ID is valid
        items = Item.objects.filter(pk=item_id)
        item_id_exists = len(items) == 1
        if not item_id_exists:
            raise Http404()
        item = items[0]

        # Check if the item is on offer
        if not item.on_offer:
            raise Http404()

        # Recreate the form
        purchases = Sale.objects.filter(buyer=buyer, purchase=item)
        choices = calculate_choices(buyer, item, purchases)
        form = BuyForm(choices, data=request.POST)

        # Check the quantity and available fund
        try:
            quantity = int(form.data["quantity"])
            if buyer.balance < quantity * item.price:
                # Recreate the form (so the user cannot buy it again)
                purchases = Sale.objects.filter(buyer=buyer, purchase=item)
                choices = calculate_choices(buyer, item, purchases)

                if len(choices) > 0:
                    form = BuyForm(choices)
                else:
                    form = False
                
                # Return
                response = render(
                    request, "store/buy-form.html", {"form": form, "item": item}
                )
                response['HX-Trigger'] = "rebalance"
                return response
        except ValidationError:
            raise Http404()

        # If everything is valid
        if form.is_valid():
            # Store the data for the QR codes
            data = []

            # Get the current site (for domain, bank)
            site = get_current_site(request)

            # Create Sale objects...
            for _ in range(quantity):
                # A new sale object with quantity 1
                sale = Sale.objects.create(
                    purchase = item,
                    buyer = buyer,
                    quantity = 1
                )

                # Save it
                sale.save()

                # Generate a token for the QR code based on
                # the sale id and the buyer id
                try:
                    fact = f"{sale.pk}#{buyer.pk}"
                    cipher_suite = Fernet(settings.KEY)
                    encrypted_fact = cipher_suite.encrypt(fact.encode("ascii"))
                    encrypted_fact = base64.urlsafe_b64encode(encrypted_fact).decode("ascii")
                    data.append(f"{site.domain}/vendor/{encrypted_fact}")
                except Exception:
                    raise Http404()

            # Decrease the balance of the buyer and increase the bank's balance
            buyer.balance = buyer.balance - item.price * quantity
            site.moderation.bank += item.price * quantity

            # Reduce the stock of the item by the sale quantity
            item.stock = item.stock - quantity

            # Save everything
            item.save()
            buyer.save()
            site.moderation.save()

            # Send the email with the QR codes
            send_QRcode(buyer.email, data)

            # Create a notification
            notification = Notification.objects.create(
                user_id=buyer,
                title=f"New purchase",
                content=(
                    (f"Thank you for buying {item.item_name}."
                    f" Check your email for the redeemable QR code.")
                ),
                link="",
            )
            notification.save()

            # Recreate the form (so the user can buy it again)
            purchases = Sale.objects.filter(buyer=buyer, purchase=item)
            choices = calculate_choices(buyer, item, purchases)

            if len(choices) > 0:
                form = BuyForm(choices)
            else:
                form = False
            
            # Return
            response = render(
                request, "store/buy-form.html", {"form": form, "item": item}
            )
            response['HX-Trigger'] = "rebalance"
            return response

    # If it is not POST
    raise Http404()


def send_QRcode(email, data):
    """Create qr code(s) from the data and send them"""

    subject = "Aidoo Shop Purchase"
    body = "here is the QR code for the purchase"

    # Create a msg that can have an image attached
    msg = EmailMultiAlternatives(subject,body,from_email=None,to=[email])
    msg.mixed_subtype = 'related'

    # Generate the qr code(s) and attach them to the email
    for count, fact in enumerate(data):
        # Pass in the URL to calculate the QR code image bytes
        qr = qrcode.make(fact)

        # Create a BytesIO to temporarily store the generated image data
        buf = BytesIO()

        # Put the image bytes into a BytesIO for temporary storage
        qr.save(buf)

        # Get the image from the buffer
        image_stream = buf.getvalue()

        # Create the image
        img = MIMEImage(image_stream, 'jpg')
        img.add_header('Content-Id', '<qr>')
        img.add_header("Content-Disposition", "inline", filename=f"qr-{count+1}.jpg")

        # Attach image to the message
        msg.attach(img)

    # Send the message
    msg.send()


class TransferView(View):
    """Displays a form for transferring coins."""

    form_class = TransferForm
    template_name = "store/transfer.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        me = request.user

        if form.is_valid():
            # Add the sender and recipient to the form
            transfer = form.save(commit=False)
            transfer.sender = me

            # We can use this since there is a validator
            recipient = User.objects.get(username=form.cleaned_data["recipient"])
            transfer.recipient = recipient

            # Check the balance
            amount = form.cleaned_data["amount"]
            if me.balance < amount:
                form.add_error("amount", "You do not have sufficient funds")
                return render(request, self.template_name, {"form": form})

            # Move the coins and save the models
            me.balance -= amount
            recipient.balance += amount
            me.save()
            recipient.save()
            transfer.save()

            # Create a notification for the recipient
            notification = Notification.objects.create(
                user_id=recipient,
                title=f"Gift from {me.username}",
                content=(
                    f"The user {me.username} gave you a gift of {amount} doos."
                ),
                link="profile/me",
            )
            notification.save()

            # No content but trigger rebalance
            return HttpResponse(
                status=204, headers={"HX-Trigger": "rebalance"}
            )

        return render(request, self.template_name, {"form": form})
