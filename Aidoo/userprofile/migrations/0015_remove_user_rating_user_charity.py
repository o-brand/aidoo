# Generated by Django 4.1.6 on 2023-03-08 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0014_user_super_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='rating',
        ),
        migrations.AddField(
            model_name='user',
            name='charity',
            field=models.BooleanField(default=False),
        ),
    ]
