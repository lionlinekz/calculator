# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0005_task_allocation'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskitem',
            name='extra',
            field=models.BooleanField(default=False),
        ),
    ]
