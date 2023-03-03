# Generated by Django 4.1.6 on 2023-03-03 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0007_rename_commeter_comment_commenter_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('AP', 'Applied'), ('RE', 'Rejected'), ('AC', 'Accepted'), ('WD', 'Withdrawn'), ('DN', 'Done'), ('CO', 'Conflict'), ('CA', 'Cancelled')], default='AP', max_length=2),
        ),
    ]
