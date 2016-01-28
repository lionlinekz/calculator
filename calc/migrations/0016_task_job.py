# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0015_remove_task_job'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='job',
            field=models.ForeignKey(default=1, to='calc.Job'),
        ),
    ]
