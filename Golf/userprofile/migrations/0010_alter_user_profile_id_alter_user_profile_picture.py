# Generated by Django 4.1.6 on 2023-02-24 14:14

from django.db import migrations, models
import userprofile.models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0009_user_profile_id_user_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_id',
            field=models.ImageField(default='ids/empty.png', upload_to=userprofile.models.profile_id_rename),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(default='profilepics/default.png', upload_to=userprofile.models.profile_picture_rename),
        ),
    ]