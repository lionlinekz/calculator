# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-28 05:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0012_auto_20160127_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='job',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='calc.Job'),
        ),
    ]
