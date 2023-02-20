# Generated by Django 4.1.3 on 2023-02-19 16:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("userprofile", "0003_user_biography_user_frozen_balance"),
    ]

    operations = [
        migrations.CreateModel(
            name="Notifications",
            fields=[
                (
                    "notification_id",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                ("content", models.CharField(max_length=100)),
                ("link", models.CharField(max_length=50)),
                ("seen", models.BooleanField(default=False)),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
