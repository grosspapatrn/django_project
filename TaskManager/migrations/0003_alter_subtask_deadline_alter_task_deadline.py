# Generated by Django 5.2.3 on 2025-06-19 16:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskManager', '0002_alter_category_options_alter_subtask_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtask',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2025, 6, 20, 16, 17, 51, 271457, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2025, 6, 20, 16, 17, 51, 271457, tzinfo=datetime.timezone.utc)),
        ),
    ]
