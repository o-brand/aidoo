# Generated by Django 4.1.6 on 2023-03-08 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0003_remove_report_report_id_report_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='id',
        ),
        migrations.AddField(
            model_name='report',
            name='report_id',
            field=models.BigAutoField(default=None, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]