import datetime
from faker import Faker
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from Golf.utils import LoginRequiredTestCase
from store.models import Item, Sale


# Get actual user model.
User = get_user_model()


class RedeemCallTestCase(LoginRequiredTestCase):
    """Tests for redeem button."""

    def setUp(self):
        fake = Faker()

        # Login from super...
        super().setUp()

        # Image...
        upload_file = open('../fortest.jpeg', 'rb')

        # Write 1 item into the item model
        item = dict()
        item["item_name"] = "language class"
        item["description"] = "Lorem ipsum..."
        item["price"] = 5
        item["stock"] = 5
        item["on_offer"] = True
        item["item_picture"] = SimpleUploadedFile(upload_file.name, upload_file.read())
        self.item = Item.objects.create(**item)

        # Write 1 sale into the sale model
        sale = dict()
        sale["purchase"] = self.item
        sale["buyer"] = self.user
        self.sale = Sale.objects.create(**sale)

    def test_page(self):
        # test availability via URL
        response = self.client.get("/vendor/redeem")
        self.assertEqual(response.status_code, 404)

    def test_page_available_by_name(self):
        # test availability via name of page
        response = self.client.get(reverse("redeem-item"))
        self.assertEqual(response.status_code, 404)

    def test_page_post_no_sale(self):
        # test without sending a sale id
        response = self.client.post("/vendor/redeem")
        self.assertEqual(response.status_code, 404)

    def test_page_post_sale_not_valid(self):
        # test with a wrong sale id
        response = self.client.post("/vendor/redeem", {"sale": 5})
        self.assertEqual(response.status_code, 404)

    def test_page_post_user_not_valid(self):
        # test with a wrong user id
        response = self.client.post("/vendor/redeem", {"sale": 1, "buyer": 0})
        self.assertEqual(response.status_code, 404)

    def test_page_post_user_not_buyer(self):
        # test with a wrong buyer id
        credentials = {
            "username": "asd2",
            "password": "asd123",
            "date_of_birth": datetime.datetime.now(),
        }
        user = User.objects.create_user(**credentials)

        response = self.client.post("/vendor/redeem", {"sale": 1, "buyer": user.pk})
        self.assertEqual(response.status_code, 404)

    def test_page_post_fine(self):
        # test works
        response = self.client.post("/vendor/redeem", {"sale": 1, "buyer": 1})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="vendor/redeemed.html")
        self.assertTrue(Sale.objects.get(pk=1).redeemed)
