from django.test import TestCase
from Golf.utils import LoginRequiredTestCase
from django.db import models
from jobs.models import Job

class TestCaseReporting(LoginRequiredTestCase):
    """ tests for the reports model """

    def setUp(self):
        # setup these things
        # users
        # jobs
        # require being logged in

        super().setUp()
        pass

    def insertion(self):
        # insert a report
        pass

    def deletion(self):
        # delete a report
        pass

    def resolution(self):
        # change the status of the report
        pass
