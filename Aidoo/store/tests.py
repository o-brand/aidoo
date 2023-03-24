import datetime
from faker import Faker
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from Aidoo.utils import LoginRequiredTestCase
from .forms import TransferForm, BuyForm
from .models import Item, Sale, Transfer
from .views import send_QRcode


# Get actual user model.
User = get_user_model()


class TransferTestCase(LoginRequiredTestCase):
    """Tests for transferring coins"""

    def setUp(self):
        super().setUp()

        fake = Faker()

        for _ in range(2):
            credentials = dict()
            credentials["username"] = fake.unique.name()
            credentials["password"] = "0"
            credentials["last_name"] = lambda: fake.last_name()
            credentials["first_name"] = lambda: fake.first_name()
            credentials["date_of_birth"] = datetime.datetime.now()
            credentials["profile_id"] = "media/profilepics/default"
            User.objects.create_user(**credentials)

    def test_transfer_page(self):
        # test availability via URL
        response = self.client.get("/store/transfer")
        self.assertEqual(response.status_code, 200)

    def test_transfer_page_address(self):
        # test availability via URL
        response = self.client.get("/store/transfer")
        self.assertTemplateUsed(response, template_name="store/transfer.html")

    def test_transfer_page_available_by_name(self):
        # test availability via name of page
        response = self.client.get(reverse("transfer"))
        self.assertEqual(response.status_code, 200)

    def test_redirect_since_everything_is_correct(self):
        # test if the user is redirected if the fields are filled in with valid data
        original_balance = User.objects.get(pk=2).balance
        new_form = {
            "recipient": User.objects.get(pk=2),
            "amount": "10",
            "note": "A little gift for you",
        }
        response = self.client.post(reverse("transfer"), data=new_form)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(User.objects.get(pk=2).balance, original_balance + 10)

    def test_no_fund(self):
        # test if the user has no sufficient fund
        new_form = {
            "recipient": User.objects.get(pk=2),
            "amount": "999",
            "note": "A little gift for you",
        }
        response = self.client.post(reverse("transfer"), data=new_form)
        self.assertEqual(response.status_code, 200)  # No fund error...

    def test_empty_form(self):
        # behaviour if empty form is submitted
        form = TransferForm(data={"something": "xyz"})

        self.assertEqual(2, len(form.errors))

        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn("This field is required", form.errors[key][0])

    def test_missing_amount_form(self):
        # behaviour if amount ism missing from form
        form = TransferForm(
            data={
                "recipient": User.objects.get(pk=2).username,
            }
        )

        self.assertEqual(1, len(form.errors))

        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn("This field is required", form.errors[key][0])

    def test_incorrect_username_form(self):
        # behaviour if recipient username doesn't exist
        form = TransferForm(
            data={
                "recipient": "nobody",
                "amount": "10",
                "note": "A little gift for you",
            }
        )

        self.assertEqual(1, len(form.errors))

        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))
            self.assertIn(
                "There is no user with the username nobody.", form.errors[key][0]
            )

    def test_gifting_for_myself(self):
        # test if the user tries t gift themselves
        original_balance = User.objects.get(pk=1).balance
        new_form = {
            "recipient": User.objects.get(pk=1),
            "amount": "24",
            "note": "A little gift for you",
        }
        response = self.client.post(reverse("transfer"), data=new_form)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(User.objects.get(pk=1).balance, original_balance)

    def test_form_is_not_valid(self):
        # test if the user tries t gift themselves
        new_form = {
            "recipient": User.objects.get(pk=1),
            "note": "A little gift for you",
        }
        response = self.client.post(reverse("transfer"), data=new_form)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="store/transfer.html")


class StoreTestCase(LoginRequiredTestCase):
    """Tests for the store front page."""

    def test_store_page(self):
        # test availability via URL
        response = self.client.get("/store/")
        self.assertEqual(response.status_code, 200)

    def test_store_page_address(self):
        # test availability via URL
        response = self.client.get("/store/")
        self.assertTemplateUsed(response, template_name="store/index.html")

    def test_store_page_available_by_name(self):
        # test availability via name of page
        response = self.client.get(reverse("store"))
        self.assertEqual(response.status_code, 200)

    def test_store_page_with_items(self):
        # test with items
        item = Item.objects.create(
            item_name="Test Item",
            description="A test item for the shop",
            price=10,
            stock=5,
            on_offer=True,
            limit_per_user=None,
            item_picture="media/profilepics/default",
        )
        Item.objects.create(
            item_name="Test Item2",
            description="A test item for the shop",
            price=10,
            stock=0,
            on_offer=True,
            limit_per_user=2,
            item_picture="media/profilepics/default",
        )
        Sale.objects.create(
            purchase=item, buyer=self.user, quantity=2,
            time_of_sale=timezone.now()
        )

        response = self.client.get(reverse("store"))
        self.assertEqual(response.status_code, 200)


class ItemModelTest(TestCase):
    """Test the Item model."""

    def setUp(self):
        """Create an Item object to be used for testing."""
        self.item = Item.objects.create(
            item_name="Test Item",
            description="A test item for the shop",
            price=10,
            stock=5,
            on_offer=True,
            limit_per_user=2,
        )

    def test_item_creation(self):
        """Test that an Item can be created and saved."""
        item_count = Item.objects.count()
        self.assertEqual(item_count, 1)

    def test_item_attributes_name(self):
        """Test that the Item attributes are correct."""
        item = Item.objects.get(item_name="Test Item")
        self.assertEqual(item.item_name, "Test Item")

    def test_item_attributes_description(self):
        """Test that the Item attributes are correct."""
        item = Item.objects.get(item_name="Test Item")
        self.assertEqual(item.description, "A test item for the shop")

    def test_item_attributes_price(self):
        """Test that the Item attributes are correct."""
        item = Item.objects.get(item_name="Test Item")
        self.assertEqual(item.price, 10)

    def test_item_attributes_stock(self):
        """Test that the Item attributes are correct."""
        item = Item.objects.get(item_name="Test Item")
        self.assertEqual(item.stock, 5)

    def test_item_attributes_on_offer(self):
        """Test that the Item attributes are correct."""
        item = Item.objects.get(item_name="Test Item")
        self.assertEqual(item.on_offer, True)

    def test_item_attributes_limit(self):
        """Test that the Item attributes are correct."""
        item = Item.objects.get(item_name="Test Item")
        self.assertEqual(item.limit_per_user, 2)


class SaleModelTest(LoginRequiredTestCase):
    """Test the Sale model."""

    def setUp(self):
        super().setUp()
        """Create an Item object and a User object to be used for testing."""
        self.item = Item.objects.create(
            item_name="Test Item",
            description="A test item for the shop",
            price=10,
            stock=5,
            on_offer=True,
            limit_per_user=2,
        )

        self.sale = Sale.objects.create(
            purchase=self.item, buyer=self.user, quantity=2,
            time_of_sale=timezone.now()
        )

    def test_sale_creation(self):
        """Test that a Sale can be created and saved."""
        sale_count = Sale.objects.count()
        self.assertEqual(sale_count, 1)

    def test_sale_attributes_purchase(self):
        """Test that the sale item is correct."""
        self.assertEqual(self.sale.purchase, self.item)

    def test_sale_attributes_buyers(self):
        """Test that the buyer is correct."""
        self.assertEqual(self.sale.buyer, self.user)

    def test_sale_attributes_quantity(self):
        """Test that the time of quantity is correct."""
        self.assertEqual(self.sale.quantity, 2)

    def test_sale_attributes_time_of_sale(self):
        """Test that the time of sale is correct."""
        self.assertIsNotNone(self.sale.time_of_sale)


class BuyFormTestCase(TestCase):
    """Tests for BuyForm"""

    def test_quantity_in_range(self):
        buy = {
            "quantity":"1"
        }
        form = BuyForm(['1'], data=buy)

        self.assertEqual(0, len(form.errors))

    def test_quantity_out_of_range(self):
        buy = {
            "quantity":"3"
        }
        form = BuyForm(['1'], data=buy)

        self.assertEqual(1, len(form.errors))

        for key in form.errors:
            error_now = form.errors[key]
            self.assertEqual(1, len(error_now))

            if key == "quantity":
                self.assertIn(
                    "Select a valid choice. 3 is not one of the available choices.",
                    form.errors[key][0]
                )


class SendQRCodeTestCase(TestCase):
    """Tests for send_QRcode function"""

    def test_function(self):
        # Call the function and check if the email was sent
        send_QRcode("asd@asd.com", "Asd", ["0", "1"])

        # Test email was sent
        self.assertEqual(len(mail.outbox), 1)
