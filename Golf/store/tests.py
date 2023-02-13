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

# TODO tests
class StoreTestCase(TestCase):
    pass
    # def test_store_page(self):
    #     # test availability via URL
    #     response = self.client.get("/store")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, template_name="store/storefront.html")

    # def test_store_page_available_by_name(self):
    #     # test availability via name of page
    #     response = self.client.get(reverse("store"))
    #     self.assertEqual(response.status_code, 200)
