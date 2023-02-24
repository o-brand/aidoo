# Generated by Django 4.1.6 on 2023-02-24 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0008_alter_user_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_id',
            field=models.ImageField(default='ids/empty.jpg', upload_to='ids/'),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(default='profilepics/default.png', upload_to='profilepics/'),
        ),
    ]
