# Generated by Django 4.1.2 on 2022-10-26 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_jobposting_poster_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobposting',
            name='location',
            field=models.CharField(max_length=8),
        ),
    ]