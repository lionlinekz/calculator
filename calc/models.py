from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Contract(models.Model):
    price = 0

    def __unicode__(self):
        return self.price

class Task(models.Model):
	site = models.IntegerField(default=0)
	stage = models.CharField(max_length=128)
	item_no = models.CharField(max_length=10)
	task_name = models.CharField(max_length=256)
	costs_estimated = models.FloatField(default=0)
	costs_quoted = models.FloatField(default=0)
	highest_quote = models.FloatField(default =0)
	expense_incurred = models.FloatField(default=0)
	task_complete = models.BooleanField(default=False)
	under_quote_by = models.FloatField(default=0)
	under_quote_by2 = models.FloatField(default=0)
	expense_future_calculator = models.FloatField(default=0)
	expense_future = models.FloatField(default = 0)
	infront_cost = models.FloatField(default=0)
	client_charged = models.FloatField(default=0)
	payment_received = models.FloatField(default=0)
	payment_date = models.DateField(default=datetime.now)

	class Meta:
		unique_together = ('item_no', 'stage', 'site', 'task_name')

	def __unicode__(self):
		return self.task_name

class TaskItem(models.Model):
	task = models.ForeignKey(Task)
	item_no = models.CharField(max_length=256)
	item_name = models.CharField(max_length=256)
	expense_incurred = models.CharField(max_length=256)
	invoice_no = models.CharField(max_length=256)
	trade_contractor = models.CharField(max_length=256)
	contractor_paid = models.FloatField()
	contractor_paid_date = models.DateField()
	allocation = models.FloatField()

	class Meta:
		unique_together = ('item_no', 'invoice_no', 'contractor_paid_date')


	def __unicode__(self):
		return self.item_name
