# Generated by Django 4.1.6 on 2023-02-10 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='opt_in_emails',
            field=models.BooleanField(default=True),
        ),
    ]