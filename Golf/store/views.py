from io import BytesIO
import qrcode
import mimetypes
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.views import View
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

    items = Item.objects.filter(on_offer=True)
    purchases = Sale.objects.filter(buyer=request.user)
    purchased_items = [x.purchase for x in purchases]

    forms = dict()
    for k in items:
        values = range(1,min(k.limit_per_user - sum(
            [x.quantity for x in Sale.objects.filter(
                purchase=k, buyer=request.user)]),
            k.stock, 5)+1 if k.limit_per_user is not None else min(5, k.stock)+1)
        if len(values) > 0:
            forms[k] = BuyForm(values)
        else:
            print("hi")
            forms[k] = False

    # forms = {
    #     k:
    #     BuyForm(range(1,min(
    #         k.limit_per_user - sum([x.quantity for x in Sale.objects.filter(
    #             purchase=k, buyer=request.user)]),
    #         k.stock)+1
    #     if k.limit_per_user is not None else k.stock)) for k in items
    # }

    context = {
        "items": items,
        "purchases": purchased_items,
        "forms": forms,
    }
    return render(request, "store/storefront.html", context)

def buyitem_call(request):
    if request.method == 'POST':
        user = request.user
        buyer = User.objects.get(id=user.id)

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

        choices = range(1,min(
            item.limit_per_user - sum([x.quantity for x in Sale.objects.filter(
                purchase=item, buyer=request.user)]), item.stock)+1
            if item.limit_per_user is not None else item.stock)
        
        form = BuyForm(choices, data=request.POST)
        if form.is_valid():
            sale = Sale.objects.create(
            purchase = item,
            buyer = buyer,
            quantity = int(form.cleaned_data["quantity"]))

            buyer.balance = buyer.balance - item.price * sale.quantity
            # Reduce the stock of the item by the sale qty
            item.stock = item.stock - sale.quantity

            send_QRcode(buyer.email, sale.pk)

            item.save()
            buyer = buyer.save()
            sale = sale.save()

    return HttpResponse(status=204)


def buyitem(request):
    """User buys an item from the store"""
    if request.method == "POST":
        # Get the item ID or -1 if it is not found
        item_id = request.POST.get("item_id", -1)
        buyer = request.user

        # Check if the item ID is valid
        items = Item.objects.filter(pk=item_id)
        item_id_exists = len(items) == 1
        if not item_id_exists:
            raise Http404()
        item = items[0]

        if not item.on_offer:
            raise Http404()

        # Get quantity
        try:
            quantity = int(request.POST.get("quantity", -1))
        except ValueError:
            raise Http404()
        if quantity <= 0:
            raise Http404()

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

        send_QRcode(buyer.email, sale.pk)

        return render(request, "htmx/buy-item-bought.html")

    # If it is not POST
    raise Http404()

def send_QRcode(email, data):
    """ create a qr code from the data and return an image stream """
    qr = qrcode.make(data)           # pass in the URL to calculate the QR code image bytes
    buf = BytesIO()                      # Create a BytesIO to temporarily store the generated image data
    qr.save(buf)                        # Put the image bytes into a BytesIO for temporary storage
    image_stream = buf.getvalue()

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
    img = MIMEImage(image_stream, 'jpg')
    img.add_header('Content-Id', '<qr>')
    img.add_header("Content-Disposition", "inline", filename="qr.jpg")

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
            ) # No content

        return render(
            request, self.template_name, {"form": form}
        )
