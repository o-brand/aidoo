# Generated by Django 4.1.6 on 2023-02-20 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0004_notifications'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Notifications',
            new_name='Notification',
        ),
    ]