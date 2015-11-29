# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('site', models.IntegerField(default=0)),
                ('stage', models.CharField(max_length=128)),
                ('item_no', models.CharField(max_length=10)),
                ('task_name', models.CharField(max_length=256)),
                ('costs_estimated', models.FloatField(default=0)),
                ('costs_quoted', models.FloatField(default=0)),
                ('highest_quote', models.FloatField(default=0)),
                ('expense_incurred', models.FloatField(default=0)),
                ('task_complete', models.BooleanField(default=False)),
                ('under_quote_by', models.FloatField(default=0)),
                ('under_quote_by2', models.FloatField(default=0)),
                ('expense_future_calculator', models.FloatField(default=0)),
                ('expense_future', models.FloatField(default=0)),
                ('infront_cost', models.FloatField(default=0)),
                ('client_charged', models.FloatField(default=0)),
                ('payment_received', models.FloatField(default=0)),
                ('payment_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='TaskItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_no', models.CharField(max_length=256)),
                ('item_name', models.CharField(max_length=256)),
                ('expense_incurred', models.CharField(max_length=256)),
                ('invoice_no', models.CharField(max_length=256)),
                ('trade_contractor', models.CharField(max_length=256)),
                ('contractor_paid', models.FloatField()),
                ('contractor_paid_date', models.DateField()),
                ('allocation', models.FloatField()),
                ('task', models.ForeignKey(to='calc.Task')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='task',
            unique_together=set([('task_name', 'item_no')]),
        ),
        migrations.AlterUniqueTogether(
            name='taskitem',
            unique_together=set([('item_no', 'invoice_no', 'contractor_paid_date')]),
        ),
    ]
