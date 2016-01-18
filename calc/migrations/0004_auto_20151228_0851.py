# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0003_auto_20151212_0554'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='task',
            unique_together=set([('item_no', 'stage', 'site', 'task_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='taskitem',
            unique_together=set([('item_no', 'invoice_no', 'contractor_paid_date')]),
        ),
    ]
