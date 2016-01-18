# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0002_auto_20151212_0549'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='taskitem',
            unique_together=set([]),
        ),
    ]
