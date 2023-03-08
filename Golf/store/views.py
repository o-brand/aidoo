from io import BytesIO
import math
import qrcode
import mimetypes
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.views import View
from django.core.exceptions import ValidationError
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
from .models import Item, Sale
from .models import Item, Sale, Transfer
from userprofile.models import Notification
from .forms import TransferForm, BuyForm


# Get actual user model.
User = get_user_model()


def home(request):
    # Render the main shop page
    actual_user_id = request.user.id

    # Check if the user ID is valid
    users = User.objects.filter(pk=actual_user_id)
    user_id_exists = len(users) == 1
    if not user_id_exists:
        raise Http404()
    me = request.user

    items = Item.objects.filter(on_offer=True)
    purchases = Sale.objects.filter(buyer=me)
    purchased_items = [x.purchase for x in purchases]

    forms = dict()
    for item in items:
        # Takes the minimum of the (limit per user - already bought),
        # the stock, the display limit of 5, and the maximal quantity
        # that can be bought using the balance
        values = range(1, min(
            item.limit_per_user - sum([x.quantity for x in Sale.objects.filter(
                purchase=item, buyer=me)])
            if item.limit_per_user is not None else item.stock,
            me.balance//item.price, item.stock, 5)+1)
        if len(values) > 0:
            forms[item] = BuyForm(values)
        else:
            forms[item] = False

    context = {
        "items": items,
        "purchases": purchased_items,
        "forms": forms,
    }
    return render(request, "store/storefront.html", context)

def buyitem_call(request):
    if request.method == 'POST':
        me = request.user
        buyer = me

        try:
            item_id = int(request.POST.get("purchase", -1))
        except ValueError:
            raise Http404()

        items = Item.objects.filter(pk=item_id)
        if item_id < 0 or len(items) != 1:
            raise Http404()
        item = items[0]

        if not item.on_offer:
            raise Http404()

        choices = range(1, min(
            item.limit_per_user - sum([x.quantity for x in Sale.objects.filter(
                purchase=item, buyer=me)])
            if item.limit_per_user is not None else item.stock,
            me.balance//item.price, item.stock, 5)+1)

        form = BuyForm(choices, data=request.POST)
        try:
            quantity = int(form.data["quantity"])
            if buyer.balance < quantity * item.price:
                raise Http404()
        except ValidationError:
            raise Http404()
        if form.is_valid():
            data = []
            for _ in range(quantity):
                sale = Sale.objects.create(
                purchase = item,
                buyer = buyer,
                quantity = 1)

                sale.save()

                data.append(sale.pk)

            buyer.balance = buyer.balance - item.price * sale.quantity
            # Reduce the stock of the item by the sale qty
            item.stock = item.stock - quantity

            send_QRcode(buyer.email, data)

            item.save()
            buyer.save()

            notification = Notification.objects.create(
                user_id=me,
                title=f"New purchase",
                content=(
                    (f"Thank you for buying {item.item_name}."
                    f" Check your email for the redeemable QR code.")
                ),
                link="",
            )
            notification.save()

            return HttpResponse(
                status=204,
                headers={"HX-Trigger": "rebalance"})

    raise Http404()

def send_QRcode(email, data):
    """ create a qr code from the data and return an image stream """
    subject = "Aidoo Shop Purchase"
    body = "here is the QR code for the purchase"

    # create a msg that can have an image attached
    msg = EmailMultiAlternatives(
        subject,
        body,
        from_email=None,
        to=[email]
    )

    msg.mixed_subtype = 'related'
    # convert img to html

    for fact in data:
        qr = qrcode.make(fact)           # pass in the URL to calculate the QR code image bytes
        buf = BytesIO()                      # Create a BytesIO to temporarily store the generated image data
        qr.save(buf)                        # Put the image bytes into a BytesIO for temporary storage
        image_stream = buf.getvalue()

        img = MIMEImage(image_stream, 'jpg')
        img.add_header('Content-Id', '<qr>')
        img.add_header("Content-Disposition", "inline", filename=f"qr-{fact}.jpg")
        # attach image in html form to message
        msg.attach(img)

    # send the message
    msg.send()


class TransferView(View):
    """Displays a form for transferring coins."""

    form_class = TransferForm
    template_name = "store/transfer.html"

    def get(self, request, *args, **kwargs):
        me = request.user
        form = self.form_class(initial={"email": me.email, "biography": me.biography})
        return render(
            request, self.template_name, {"form": form, "poster_id": request.user.id}
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        me = request.user

        if form.is_valid():
            transfer = form.save(commit=False)
            transfer.sender = me
            try:
                recipient = User.objects.get(username=form.cleaned_data["recipient"])
            except User.DoesNotExist:
                form.add_error('recipient', 'This user does not exist' )
                return render(
                    request, self.template_name, {"form": form}
                )
            transfer.recipient = recipient
            transfer.save()

            amount = form.cleaned_data["amount"]
            if me.balance < amount:
                form.add_error('amount', 'You do not have sufficient funds' )
                return render(
                    request, self.template_name, {"form": form}
                )

            me.balance -= amount
            recipient.balance += amount
            me.save()
            recipient.save()

            notification = Notification.objects.create(
                user_id=recipient,
                title=f"Gift from {me.username}",
                content=(
                    f"The user {me.username} gave you a gift of " + \
                    f"{amount} doos."
                ),
                link="profile/me",
            )
            notification.save()

            return HttpResponse(
                status=204,
                headers={"HX-Trigger": "rebalance"}
            ) # No content

        return render(
            request, self.template_name, {"form": form}
        )
