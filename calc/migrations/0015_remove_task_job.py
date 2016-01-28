# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0014_auto_20160128_1022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='job',
        ),
    ]
