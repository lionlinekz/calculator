# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0013_auto_20160127_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='job',
            field=models.ForeignKey(default=1, to='calc.Job'),
        ),
    ]
