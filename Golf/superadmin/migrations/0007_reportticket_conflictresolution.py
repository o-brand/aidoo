# Generated by Django 4.1.6 on 2023-03-09 16:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobs', '0008_alter_application_status'),
        ('superadmin', '0006_remove_conflictresolution_job_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportTicket',
            fields=[
                ('ticket_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('answer', models.CharField(blank=True, choices=[('BA', 'Ban'), ('NB', 'Not_Ban')], default=None, max_length=2, null=True)),
                ('time_assigned', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('OP', 'Open'), ('RE', 'Resolved')], default='OP', max_length=2)),
                ('report_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='superadmin.report')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ConflictResolution',
            fields=[
                ('conflict_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=100)),
                ('conflict_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('conflict_update_time', models.DateTimeField(blank=True, default=None, null=True)),
                ('status', models.CharField(choices=[('Open', 'Open'), ('Flagged', 'Flagged'), ('Resolved', 'Reesolved')], default='Open', max_length=10)),
                ('type', models.CharField(choices=[('Conflict1', 'Conflict1'), ('Conflict2', 'Conflict2')], max_length=10)),
                ('job_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='jobs.job')),
                ('user1_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user1', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
