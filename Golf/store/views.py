from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import Item, Sale
from django.utils.six import BytesIO
import qrcode
import mimetypes

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

        # get the sale_id

        return render(request, "htmx/buy-item-bought.html")

    # If it is not POST
    raise Http404()


def send_QRcode(request, data):
    """ create a qr code from the data and return an image stream """
    qr = qrcode.make(data)           # pass in the URL to calculate the QR code image bytes
    buf = BytesIO()                      # Create a BytesIO to temporarily store the generated image data
    qr.save(buf)                        # Put the image bytes into a BytesIO for temporary storage
    image_stream = buf.getvalue()        # Temporarily save the data in BytesIO

    # convert the image into html
    html_part = MIMEMultipart(_subtype='related')

    body = MIMEText('<p>Hello <img src="cid:myimage" /></p>', _subtype='html')
    html_part.attach(body)

    img = MIMEImage(buf, 'jpeg')
    img.add_header('Content-Id', '<myimage>')  # angle brackets are important
    img.add_header("Content-Disposition", "inline", filename="myimage")  # David Hess recommended this edit
    html_part.attach(img)

    subject = "Aidoo Shop Purchase"
    msg = "here is the QR code for the purchase"

    send_mail(subject, msg, None, [User.email], html_message = html_part)

    response = HttpResponse(image_stream, content_type="image/jpg")       # Return the QR code data to the page
    return response
