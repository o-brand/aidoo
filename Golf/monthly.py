# python monthly.py - DO NOT RUN LOCALLY!!

import datetime

# If it is the first day of the month
if datetime.datetime.today().day == 1:

    import django

    django.setup()

    from django.contrib.auth import get_user_model
    from django.contrib.sites.models import Site
    from store.models import Moderation


    # Get actual user model.
    User = get_user_model()


    # Get charities
    charities = User.objects.filter(charity=True)
    number_of_charities = len(charities)

    # Get site with the bank's balance
    site = Site.objects.get_current().moderation

    # Calculate the donation
    donation = int(site.bank / number_of_charities)

    # Give the doos to the charities
    for charity in charities:
        charity.balance += donation
        charity.save()
        site.bank -= donation

    # Save new bank balance
    site.save()
