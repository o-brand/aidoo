# Generated by Django 4.1.6 on 2023-03-15 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0008_alter_application_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='job',
            options={'ordering': ('-posting_time',)},
        ),
    ]
