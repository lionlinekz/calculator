# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0010_auto_20160123_1024'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='idea',
            unique_together=set([('name', 'description', 'task_type')]),
        ),
    ]
