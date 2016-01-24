# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='payment_date',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterUniqueTogether(
            name='task',
            unique_together=set([]),
        ),
    ]
