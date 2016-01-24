# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0009_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('task_type', models.CharField(max_length=128)),
                ('cost', models.FloatField(default=0)),
                ('description', models.CharField(max_length=700)),
                ('status', models.CharField(max_length=128)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='task',
            unique_together=set([('item_no', 'stage', 'site', 'task_name')]),
        ),
    ]
