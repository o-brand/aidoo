# Generated by Django 4.1.6 on 2023-03-01 00:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0002_item_limit_per_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('transfer_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField()),
                ('note', models.CharField(default='', max_length=250)),
                ('time_of_transfer', models.DateTimeField(default=django.utils.timezone.now)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
