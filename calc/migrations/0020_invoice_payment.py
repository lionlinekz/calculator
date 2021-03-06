# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-11 05:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0019_auto_20160210_2134'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('value', models.FloatField(default=0)),
                ('date', models.DateField(default=datetime.datetime.now)),
                ('total_paid', models.FloatField(default=0)),
                ('stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calc.Stage')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0)),
                ('date', models.DateField(default=datetime.datetime.now)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calc.Invoice')),
            ],
        ),
    ]
