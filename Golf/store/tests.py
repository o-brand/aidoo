import datetime
import random
from faker import Faker
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from Golf.utils import create_date_string
from Golf.utils import LoginRequiredTestCase
from .models import Item, Sale


# TODO tests
class StoreTestCase(LoginRequiredTestCase):
    """TODO"""
    def setUp(self):
        super().setUp()

    def test_store_page(self):
        # test availability via URL
        response = self.client.get("/store/")
        self.assertEqual(response.status_code, 200)

    
    def test_store_page_address(self):
        # test availability via URL
        response = self.client.get("/store/")
        self.assertTemplateUsed(response, template_name="store/storefront.html")

    def test_store_page_available_by_name(self):
        # test availability via name of page
        response = self.client.get(reverse("store"))
        self.assertEqual(response.status_code, 200)


# Get actual user model.
User = get_user_model()

class ItemModelTest(TestCase):
    """Test the Item model."""

    def setUp(self):
        """Create an Item object to be used for testing."""
        self.item = Item.objects.create(
            item_name='Test Item',
            description='A test item for the shop',
            price=10,
            stock=5,
            on_offer=True,
            limit_per_user=2
        )

    def test_item_creation(self):
        """Test that an Item can be created and saved."""
        item_count = Item.objects.count()
        self.assertEqual(item_count, 1)

    def test_item_attributes_name(self):
        """Test that the Item attributes are correct."""
        item = Item.objects.get(item_name='Test Item')
        self.assertEqual(item.item_name, 'Test Item')

    def test_item_attributes_description(self):
        """Test that the Item attributes are correct."""
        item = Item.objects.get(item_name='Test Item')
        self.assertEqual(item.description, 'A test item for the shop')

    def test_item_attributes_price(self):
        """Test that the Item attributes are correct."""
        item = Item.objects.get(item_name='Test Item')       
        self.assertEqual(item.price, 10)

    def test_item_attributes_stock(self):
        """Test that the Item attributes are correct."""
        item = Item.objects.get(item_name='Test Item')  
        self.assertEqual(item.stock, 5)
        
    def test_item_attributes_on_offer(self):
        """Test that the Item attributes are correct."""
        item = Item.objects.get(item_name='Test Item')       
        self.assertEqual(item.on_offer, True)

    def test_item_attributes_limit(self):
        """Test that the Item attributes are correct."""
        item = Item.objects.get(item_name='Test Item')       
        self.assertEqual(item.limit_per_user, 2)

class SaleModelTest(LoginRequiredTestCase):
    """Test the Sale model."""

    def setUp(self):
        super().setUp()
        """Create an Item object and a User object to be used for testing."""
        self.item = Item.objects.create(
            item_name='Test Item',
            description='A test item for the shop',
            price=10,
            stock=5,
            on_offer=True,
            limit_per_user=2
        )


    def test_sale_creation(self):
        """Test that a Sale can be created and saved."""
        sale = Sale.objects.create(
            purchase=self.item,
            buyer=self.user,
            quantity=2,
            time_of_sale=timezone.now()
        )
        
        sale_count = Sale.objects.count()
        self.assertEqual(sale_count, 1)


    def test_sale_attributes_purchase(self):
        """Test that the Sale attributes are correct."""
        sale = Sale.objects.create(
            purchase=self.item,
            buyer=self.user,
            quantity=2,
            time_of_sale=timezone.now()
        )
        self.assertEqual(sale.purchase, self.item)
        
    def test_sale_attributes_buyers(self):
        """Test that the Sale attributes are correct."""
        sale = Sale.objects.create(
            purchase=self.item,
            buyer=self.user,
            quantity=2,
            time_of_sale=timezone.now()
        )
        self.assertEqual(sale.buyer, self.user)

    def test_sale_attributes_quantity(self):
        """Test that the Sale attributes are correct."""
        sale = Sale.objects.create(
            purchase=self.item,
            buyer=self.user,
            quantity=2,
            time_of_sale=timezone.now()
        )
        self.assertEqual(sale.quantity, 2)

    def test_sale_attributes_time_of_sale(self):
        """Test that the Sale attributes are correct."""
        sale = Sale.objects.create(
            purchase=self.item,
            buyer=self.user,
            quantity=2,
            time_of_sale=timezone.now()
        )
        self.assertIsNotNone(sale.time_of_sale)
