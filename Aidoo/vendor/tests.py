import base64
import datetime
from cryptography.fernet import Fernet
from faker import Faker
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from Aidoo.utils import LoginRequiredTestCase
from store.models import Item, Sale


# Get actual user model.
User = get_user_model()


class RedeemTestCase(TestCase):
    """Tests for displaying the redeem page."""

    def setUp(self):
        # Create a user.
        credentials = {
            "username": "asd",
            "password": "asd123",
            "date_of_birth": datetime.datetime.now(),
            "profile_id": "media/profilepics/default",
        }
        self.user = User.objects.create_user(**credentials)

        # Write 1 item into the item model.
        item = dict()
        item["item_name"] = "language class"
        item["description"] = "Lorem ipsum..."
        item["price"] = 5
        item["stock"] = 5
        item["on_offer"] = True
        item["item_picture"] = "media/profilepics/default"
        self.item = Item.objects.create(**item)

        # Write 1 sale into the sale model.
        sale = dict()
        sale["purchase"] = self.item
        sale["buyer"] = self.user
        sale["quantity"] = 1
        self.sale = Sale.objects.create(**sale)

        # Create a valid token
        fact = "1#1"
        cipher_suite = Fernet(settings.KEY)
        encrypted_fact = cipher_suite.encrypt(fact.encode("ascii"))
        self.token = base64.urlsafe_b64encode(encrypted_fact).decode("ascii")

    def test_redeem_page_invalid_token(self):
        # Test with an invalid token
        response = self.client.get("/vendor/" + self.token[:-1])
        self.assertEqual(response.status_code, 404)

    def test_redeem_page(self):
        # Test if the page is available with a valid token
        response = self.client.get("/vendor/" + self.token)
        self.assertEqual(response.status_code, 200)

    def test_redeem_page_available_by_name(self):
        # Test if the page is available by name with a valid token
        response = self.client.get(
            reverse("redeem", kwargs={"token": self.token})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="vendor/index.html")

    def test_redeem_page_wrong_buyer(self):
        # Test if the given buyer is not the actual buyer
        fact = "1#2"
        cipher_suite = Fernet(settings.KEY)
        encrypted_fact = cipher_suite.encrypt(fact.encode("ascii"))
        token = base64.urlsafe_b64encode(encrypted_fact).decode("ascii")

        # Create another user.
        credentials = {
            "username": "asdasd",
            "password": "asd123",
            "date_of_birth": datetime.datetime.now(),
            "profile_id": "media/profilepics/default",
        }
        User.objects.create_user(**credentials)

        response = self.client.get(
            reverse("redeem", kwargs={"token": token})
        )
        self.assertEqual(response.status_code, 404)


class RedeemCallTestCase(LoginRequiredTestCase):
    """Tests for redeem button."""

    def setUp(self):
        fake = Faker()

        # Login from super...
        super().setUp()

        # Write 1 item into the item model
        item = dict()
        item["item_name"] = "language class"
        item["description"] = "Lorem ipsum..."
        item["price"] = 5
        item["stock"] = 5
        item["on_offer"] = True
        item["item_picture"] = "media/profilepics/default"
        self.item = Item.objects.create(**item)

        # Write 1 sale into the sale model
        sale = dict()
        sale["purchase"] = self.item
        sale["buyer"] = self.user
        sale["quantity"] = 1
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
            "profile_id": "media/profilepics/default",
        }
        user = User.objects.create_user(**credentials)

        response = self.client.post(
            "/vendor/redeem", {"sale": 1, "buyer": user.pk}
        )
        self.assertEqual(response.status_code, 404)

    def test_page_post_fine(self):
        # test works
        response = self.client.post("/vendor/redeem", {"sale": 1, "buyer": 1})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, template_name="vendor/redeemed.html"
        )
        self.assertTrue(Sale.objects.get(pk=1).redeemed)
