# Generated by Django 4.1.6 on 2023-02-23 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0006_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='commeter',
            new_name='commenter_id',
        ),
    ]