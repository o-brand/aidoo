# Generated by Django 4.1.6 on 2023-03-06 22:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('superadmin', '0004_merge_20230306_2250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conflictresolution',
            name='conflict_id',
        ),
        migrations.AddField(
            model_name='conflictresolution',
            name='id',
            field=models.BigAutoField(auto_created=True, default=None, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reportticket',
            name='answer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reportticket',
            name='report_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='superadmin.report'),
        ),
        migrations.AddField(
            model_name='reportticket',
            name='time_assigned',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='reportticket',
            name='time_resolved',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='reportticket',
            name='user_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
