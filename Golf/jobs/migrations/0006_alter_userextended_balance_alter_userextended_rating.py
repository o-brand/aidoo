# Generated by Django 4.2.dev20221012095013 on 2022-11-02 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_alter_jobposting_assigned_alter_jobposting_completed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextended',
            name='balance',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userextended',
            name='rating',
            field=models.FloatField(default=0),
        ),
    ]