# Generated by Django 4.1.6 on 2023-02-03 16:00

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('application_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('AP', 'Applied'), ('RE', 'Rejected'), ('AC', 'Accepted'), ('WD', 'Withdrawn'), ('DN', 'Done'), ('CO', 'Conflict')], default='AP', max_length=2)),
                ('time_of_application', models.DateTimeField(default=django.utils.timezone.now)),
                ('time_of_final_status', models.DateTimeField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('bookmark_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('saving_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('job_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=8)),
                ('job_title', models.CharField(max_length=50)),
                ('job_short_description', models.CharField(max_length=50)),
                ('job_description', models.CharField(max_length=1000)),
                ('posting_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('points', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('deadline', models.DateField(blank=True, default=None, null=True)),
                ('hidden', models.BooleanField(default=False)),
                ('assigned', models.BooleanField(default=False)),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
    ]