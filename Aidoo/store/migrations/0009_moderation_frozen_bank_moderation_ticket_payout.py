# Generated by Django 4.1.6 on 2023-03-24 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_sale_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='moderation',
            name='frozen_bank',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='moderation',
            name='ticket_payout',
            field=models.IntegerField(default=2),
        ),
    ]