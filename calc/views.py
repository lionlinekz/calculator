# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from calc.models import Task
from calc.models import TaskItem, Idea
from calc.models import Contract, WishList, Job, Invoice, Payment, Stage
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
import cStringIO as StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from cgi import escape
from django.db.models import Sum
from django.core.urlresolvers import reverse
from django import template
import xlwt

register = template.Library()
import csv


def payments(request, number=0, jid=0):
	context_dict = {}
	context_dict['stages'] = Stage.objects.all()
	context_dict['invoices'] = Invoice.objects.filter(job=jid, site=number).exclude(stage__isnull=True)
	context_dict['variations'] = Invoice.objects.filter(job=jid, site=number, stage = None)
	context_dict['payments'] = Payment.objects.all()
	job = Job.objects.get(pk=jid)
	context_dict['units'] = create_list(job.number)
	context_dict['number'] = number
	context_dict['jid'] = jid
	return render(request, 'calc/payments.html', context_dict)

def add_invoice(request, number=0, jid=0):
	if request.method == "POST":
		try:
			stage_id = request.POST['name']
			value = request.POST['value']
			date = request.POST['date']
			stage = Stage.objects.get(pk = stage_id)
			job = Job.objects.get(pk = jid)
			invoice = Invoice(job = job, site = number, stage = stage, name = stage.name, value = value, date = date)
			invoice.save()
		except Exception as e:
			print e
		url = reverse('payments', kwargs={'jid': jid, 'number':number})
		return HttpResponseRedirect(url)

def add_payment(request, number=0, jid=0):
	if request.method == "POST":
		try:
			invoice_id = request.POST['name']
			value = request.POST['value']
			date = request.POST['date']
			invoice = Invoice.objects.get(pk = invoice_id)
			payment = Payment(invoice = invoice, amount = value, date = date)
			payment.save()
			invoice.total_paid += float(value)
			invoice.save()
		except Exception as e:
			print e
		url = reverse('payments', kwargs={'jid': jid, 'number':number})
		return HttpResponseRedirect(url)

def add_variation(request, number=0, jid=0):
	if request.method == "POST":
		try:
			name = request.POST['name']
			value = request.POST['value']
			date = request.POST['date']
			job = Job.objects.get(pk = jid)
			invoice = Invoice(job = job, site = number, name = name, value = value, date = date)
			invoice.save()
		except Exception as e:
			print e
		url = reverse('payments', kwargs={'jid': jid, 'number':number})
		return HttpResponseRedirect(url)

def edit_invoice(request, number=0, jid=0):
	if request.method == "POST":
		try:
			invoice_id = request.POST['id']
			invoice = Invoice.objects.get(pk = invoice_id)
			stage_id = request.POST['name']
			value = request.POST['value']
			date = request.POST['date']
			stage = Stage.objects.get(pk = stage_id)
			job = Job.objects.get(pk = jid)
			invoice.stage = stage
			invoice.date = date
			invoice.value = value
			invoice.save()
		except Exception as e:
			print e
		url = reverse('payments', kwargs={'jid': jid, 'number':number})
		return HttpResponseRedirect(url)

def delete_invoice(request, number=0, jid=0):
	if request.method == "POST":
		invoice_id = request.POST['id']
		invoice = Invoice.objects.get(pk = invoice_id)
		invoice.delete()
		url = reverse('payments', kwargs={'jid': jid, 'number':number})
		return HttpResponseRedirect(url)

def delete_payment(request, number=0, jid=0):
	if request.method == "POST":
		payment_id = request.POST['id']
		payment = Payment.objects.get(pk = payment_id)
		invoice = payment.invoice
		invoice.total_paid -= payment.amount
		invoice.save()
		payment.delete()
		url = reverse('payments', kwargs={'jid': jid, 'number':number})
		return HttpResponseRedirect(url)

def edit_payment(request, number=0, jid=0):
	if request.method == "POST":
		try:
			payment_id = request.POST['id']
			payment = Payment.objects.get(pk = payment_id)
			value = request.POST['value']
			date = request.POST['date']
			payment.date = date
			invoice_id = payment.invoice.id
			invoice = Invoice.objects.get(pk = invoice_id)
			invoice.total_paid -= float(payment.amount)
			invoice.total_paid += float(value)
			invoice.save()
			payment.amount = value
			payment.save()
		except Exception as e:
			print e
		url = reverse('payments', kwargs={'jid': jid, 'number':number})
		return HttpResponseRedirect(url)

def edit_variation(request, number=0, jid=0):
	if request.method == "POST":
		invoice_id = request.POST['id']
		invoice = Invoice.objects.get(pk = invoice_id)
		name = request.POST['name']
		value = request.POST['value']
		date = request.POST['date']
		invoice.name = name
		invoice.date = date
		invoice.value = value
		invoice.save()
		url = reverse('payments', kwargs={'jid': jid, 'number':number})
		return HttpResponseRedirect(url)

def jobs(request):
	context_dict = {}
	context_dict['jobs'] = Job.objects.all()
	return render(request, 'calc/jobs.html', context_dict)

def add_job(request):
	if request.method == "POST":
		try:
			job = Job()
			job.name = request.POST['name']
			job.cost = request.POST['cost']
			job.address = request.POST['address']
			job.number = request.POST['number']
			job.save()
			csv_filepathname="/home/lionline/calculator/calc/data-aset.csv"
			for i in range(0, int(job.number)):
				dataReader = csv.reader(open(csv_filepathname), delimiter=';', quotechar='"')
				for row in dataReader:
					task = Task()
					task.job = job
					task.site = i
					task.stage = row[0]
					task.item_no = row[1]
					task.task_name = row[2]
					task.save()
		except Exception as e:
			print e
		return HttpResponseRedirect('/jobs/')

def ideas(request):
	context_dict = {}
	if request.method == "POST":
		try:
			name = request.POST['name']
			task_type = request.POST['type']
			cost = request.POST['cost']
			description = request.POST['description']
			idea = Idea(name = name, task_type = task_type, cost = cost, description = description)
			idea.status = "Offered"
			idea.save()
		except Exception as e:
			print e
	context_dict['ideas'] = Idea.objects.all()
	return render(request, 'calc/ideas.html', context_dict)

def edit_idea(request):
	if request.method == "POST":
		try:
			idea_id = request.POST['id']
			idea = Idea.objects.get(pk = idea_id)
			idea.name = request.POST['name']
			idea.task_type = request.POST['type']
			idea.cost = request.POST['cost']
			idea.description = request.POST['description']
			idea.status = request.POST['status']
			idea.save()
		except Exception as e:
			print e
	return HttpResponseRedirect('/ideas/')

def complete_idea(request):
	if request.method == "POST":
		try:
			idea_id = request.POST['id']
			idea = Idea.objects.get(pk = idea_id)
			idea.status = "Completed"
			idea.save()
		except Exception as e:
			print e
	return HttpResponseRedirect('/ideas/')

def delete_idea(request):
	if request.method == "POST":
		try:
			idea_id = request.POST['id']
			idea = Idea.objects.get(pk = idea_id)
			idea.delete()
		except Exception as e:
			print e
	return HttpResponseRedirect('/ideas/')


def return_html(request, context_dict):
	if request.user.is_authenticated():
		context_dict['user'] = request.user
		is_admin = request.user.groups.filter(name='Full Access').exists()
		is_input = request.user.groups.filter(name='Input Only').exists()
		is_view_all = request.user.groups.filter(name='View all').exists()
		is_view_dashboard = request.user.groups.filter(name='View dashboard').exists()		
		context_dict['is_admin'] = is_admin
		context_dict['is_input'] = is_input
		context_dict['is_view_all'] = is_view_all
		context_dict['is_view_dashboard'] = is_view_dashboard
		if request.user.groups.filter(name='Michael').exists():
			return render(request, 'calc/michael.html', context_dict)
		if request.user.groups.filter(name='Tayla').exists():
			return render(request, 'calc/tayla.html', context_dict)
		if request.user.groups.filter(name='Maria').exists():
			return render(request, 'calc/maria.html', context_dict)
		if request.user.groups.filter(name='Tracy').exists():
			return render(request, 'calc/tracy.html', context_dict)
		if request.user.groups.filter(name='Phone').exists():
			return render(request, 'calc/phone.html', context_dict)
		if request.user.groups.filter(name='Ipad').exists():
			return render(request, 'calc/ipad.html', context_dict)

@login_required(login_url='/login/')
def view_all(request, number=0, jid=0):
	job = Job.objects.get(pk=jid)
	context_dict = summary_header(number, jid)
	context_dict['tasks'] = Task.objects.filter(site=number, job=jid)
	context_dict['task_items'] = TaskItem.objects.all()
	context_dict['number'] = number
	context_dict['jid'] = jid
	context_dict['units'] = create_list(job.number)
	if request.user.is_authenticated():
		context_dict['user'] = request.user
		is_admin = request.user.groups.filter(name='Full Access').exists()
		is_input = request.user.groups.filter(name='Input Only').exists()
		is_view_all = request.user.groups.filter(name='View all').exists()
		is_view_dashboard = request.user.groups.filter(name='View dashboard').exists()		
		context_dict['is_admin'] = is_admin
		context_dict['is_input'] = is_input
		context_dict['is_view_all'] = is_view_all
		context_dict['is_view_dashboard'] = is_view_dashboard
		if request.user.groups.filter(name='Michael').exists():
			return render(request, 'calc/michael.html', context_dict)
		if request.user.groups.filter(name='Tayla').exists():
			return render(request, 'calc/tayla.html', context_dict)
		if request.user.groups.filter(name='Maria').exists():
			return render(request, 'calc/maria.html', context_dict)
		if request.user.groups.filter(name='Tracy').exists():
			return render(request, 'calc/tracy.html', context_dict)
		if request.user.groups.filter(name='Phone').exists():
			return render(request, 'calc/phone.html', context_dict)
		if request.user.groups.filter(name='Ipad').exists():
			return render(request, 'calc/ipad.html', context_dict)
	return render(request, 'calc/success.html', context_dict)

@login_required(login_url='/login/')
def view_items(request, number=0, jid=0):
	job = Job.objects.get(pk=jid)
	context_dict = summary_header(number, jid)
	context_dict['units'] = create_list(job.number)
	if request.method =='POST':
		task_id = request.POST['task_id']
		context_dict['tasks'] = Task.objects.filter(id = task_id, job=jid)
		context_dict['task_items'] = TaskItem.objects.all()
		context_dict['number'] = number
		context_dict['jid'] = jid
	if request.user.is_authenticated():
		context_dict['user'] = request.user
		is_admin = request.user.groups.filter(name='Full Access').exists()
		is_input = request.user.groups.filter(name='Input Only').exists()
		is_view_all = request.user.groups.filter(name='View all').exists()
		is_view_dashboard = request.user.groups.filter(name='View dashboard').exists()		
		context_dict['is_admin'] = is_admin
		context_dict['is_input'] = is_input
		context_dict['is_view_all'] = is_view_all
		context_dict['is_view_dashboard'] = is_view_dashboard
		if request.user.groups.filter(name='Michael').exists():
			return render(request, 'calc/michael.html', context_dict)
		if request.user.groups.filter(name='Tayla').exists():
			return render(request, 'calc/tayla.html', context_dict)
		if request.user.groups.filter(name='Maria').exists():
			return render(request, 'calc/maria.html', context_dict)
		if request.user.groups.filter(name='Tracy').exists():
			return render(request, 'calc/tracy.html', context_dict)
		if request.user.groups.filter(name='Phone').exists():
			return render(request, 'calc/phone.html', context_dict)
		if request.user.groups.filter(name='Ipad').exists():
			return render(request, 'calc/ipad.html', context_dict)
	return render(request, 'calc/success.html', context_dict)


def create_list(number):
	number_list = []
	for i in range(number):
		number_list.append(str(i))
	return number_list


@login_required(login_url='/login/')
def index(request, number=0, jid=0):
	job = Job.objects.get(pk=jid)
	context_dict = summary_header(number, jid)
	tasks = Task.objects.filter(site=number, job=jid)
	task_items = TaskItem.objects.filter(task__site=number).order_by('item_name')
	context_dict['tasks'] = tasks
	context_dict['task_items'] = task_items
	context_dict['number'] = number
	context_dict['jid'] = jid
	context_dict['units'] = create_list(job.number)
	if request.user.is_authenticated():
		context_dict['user'] = request.user
		is_admin = request.user.groups.filter(name='Full Access').exists()
		is_input = request.user.groups.filter(name='Input Only').exists()
		is_view_all = request.user.groups.filter(name='View all').exists()
		is_view_dashboard = request.user.groups.filter(name='View dashboard').exists()		
		context_dict['is_admin'] = is_admin
		context_dict['is_input'] = is_input
		context_dict['is_view_all'] = is_view_all
		context_dict['is_view_dashboard'] = is_view_dashboard
		if request.user.groups.filter(name='Michael').exists():
			return render(request, 'calc/michael.html', context_dict)
		if request.user.groups.filter(name='Tayla').exists():
			return render(request, 'calc/tayla.html', context_dict)
		if request.user.groups.filter(name='Maria').exists():
			return render(request, 'calc/maria.html', context_dict)
		if request.user.groups.filter(name='Tracy').exists():
			return render(request, 'calc/tracy.html', context_dict)
		if request.user.groups.filter(name='Phone').exists():
			return render(request, 'calc/phone.html', context_dict)
		if request.user.groups.filter(name='Ipad').exists():
			return render(request, 'calc/ipad.html', context_dict)
	return render(request, 'calc/index.html', context_dict)


@login_required(login_url='/login/')
def estimate(request, number=0, jid=0):
	context_dict = summary_header(number, jid)
	job = Job.objects.get(pk=jid)
	context_dict['jid'] = jid
	context_dict['units'] = create_list(job.number)
	tasks = Task.objects.filter(site=number, job=jid)
	task_items = TaskItem.objects.all()
	context_dict['tasks'] = tasks
	context_dict['task_items'] = task_items
	context_dict['number'] = number
	context_dict.update(summary_header(number, jid))
        if request.method == 'POST':
            try:
                for task in tasks:
                    ce = request.POST.get(str(task.id), 0.0);
                    task.costs_estimated = ce
                    task.save()
            except Exception as e:
                print e
	return render(request, 'calc/estimate.html', context_dict)

@login_required(login_url='/login/')
def start(request):
	return default(request, 0)

@login_required(login_url='/login/')
def default(request, default, jid=0):
	job = Job.objects.get(pk=jid)
	if request.method =='POST':
		price = request.POST['contract_price']
		job.cost = price
		job.save()
	context_dict = {}
	if request.user.is_authenticated():
		try:
			context_dict['user'] = request.user
			context_dict['contract_price'] = Job.objects.get(pk=jid).cost
			tasks = Task.objects.filter(job=jid)
			costs_estimated = tasks.aggregate(Sum('costs_estimated'))
			costs_quoted = tasks.aggregate(Sum('costs_quoted'))
			expense_incurred = tasks.aggregate(Sum('expense_incurred'))
			expense_future = tasks.aggregate(Sum('expense_future'))
			client_charged = tasks.aggregate(Sum('client_charged'))
			payment_received = tasks.aggregate(Sum('payment_received'))
			allocations = tasks.aggregate(Sum('allocation'))
			context_dict['costs_estimated'] = costs_estimated['costs_estimated__sum']
			context_dict['costs_quoted'] = costs_quoted['costs_quoted__sum']
			context_dict['expense_incurred'] = expense_incurred['expense_incurred__sum']
			context_dict['expense_future'] = expense_future['expense_future__sum']
			context_dict['client_charged'] = client_charged['client_charged__sum']
			context_dict['payment_received'] = payment_received['payment_received__sum']
			context_dict['allocations'] = allocations['allocation__sum']
			cost = 0
			for task in tasks:
				if task.costs_quoted == 0:
					cost = cost + task.costs_estimated
				else:
					cost = cost + task.costs_quoted
			context_dict['cost_difference_actual'] = cost - context_dict['expense_incurred']
			context_dict['profit_actual'] = int(job.cost) - expense_incurred['expense_incurred__sum']
			context_dict['profit_potential'] = int(job.cost) - costs_quoted['costs_quoted__sum']
			context_dict['profit_estimate'] = int(job.cost) - costs_estimated['costs_estimated__sum']
		except Exception as e:
			print e
		context_dict['jid'] = jid
		context_dict['units'] = range(job.number)
	return render(request, 'calc/summary.html', context_dict)


@login_required(login_url='/login/')
def add_task(request, number=0, jid=0):
	context_dict = summary_header(number, jid)
	if request.method =='POST':
		try:
			stage = request.POST['stage']
			task_number = request.POST['task_number']
			task_name = request.POST['task_name']		
			costs_estimated = request.POST['cost_estimated']
			cost_quoted = request.POST['cost_quoted']
			highest_quote = request.POST['highest_quote']
			client_charged = request.POST['client_charged']
			payment_received = request.POST['payment_received']
			payment_date = request.POST['payment_date']
			task = Task(site=number, stage=stage, item_no=task_number, task_name=task_name, costs_estimated=costs_estimated, costs_quoted=cost_quoted, highest_quote=highest_quote, client_charged=client_charged, payment_received=payment_received, payment_date=payment_date, under_quote_by=cost_quoted, under_quote_by2=cost_quoted, expense_future_calculator=cost_quoted, expense_future=cost_quoted, infront_cost=0)
			task.save()
		except Exception as e:
			print e
	return index(request, number, jid)

@login_required(login_url='/login/')
def add_item(request, number=0, jid=0):
	context_dict = summary_header(number, jid)
	if request.method =='POST':
		try:
			task_id = int(request.POST['task'])
			task = Task.objects.get(id = task_id)
			item_number = request.POST['item_number']
			item_name = request.POST['item_name']
			expense_incurred = request.POST['expense_incurred']
			invoice_number = request.POST['invoice_number']
			trade_contractor = request.POST['trade_contractor']
			contractor_paid = request.POST['contractor_paid']
			contractor_paid_date = request.POST['contractor_paid_date']
			allocation = request.POST['allocation']
			item = TaskItem(task=task, item_no=item_number, item_name=item_name, expense_incurred=expense_incurred, invoice_no=invoice_number, trade_contractor=trade_contractor, contractor_paid=contractor_paid, contractor_paid_date=contractor_paid_date, allocation=allocation)
			if task.task_complete:
				item.extra = True
				item.item_name = item_name + " EXTRA"
			item.save()	
		except Exception as e:
			print e
		update_task(task_id)
	return index(request, number, jid)

def update_task(task_id, jid=0):
	task=Task.objects.get(id = task_id)
	task_items = TaskItem.objects.filter(task=task)
	count = 0
	cost = task.costs_quoted
	for task_item in task_items:
		count = count + float(task_item.expense_incurred)
	task.expense_incurred=count
	if task.costs_quoted == 0:
            cost = task.costs_estimated
	task.under_quote_by = task.costs_estimated - task.costs_quoted
	if task.expense_incurred <= cost:
		task.under_quote_by2 = cost - task.expense_incurred
	else:
		task.under_quote_by2 = 0
	if task.task_complete:	
		task.expense_future_calculator = cost - task.expense_incurred
		task.infront_cost = task.costs_estimated - task.expense_incurred
	else:
		task.expense_future_calculator = 0
		task.infront_cost = 0

	if task.expense_future_calculator<0:
		task.expense_future = 0
	else:
		task.expense_future = task.expense_future_calculator
	task.save()
	return 0

@login_required(login_url='/login/')
def delete_task(request, number=0, jid=0):
	context_dict = summary_header(number, jid)
	if request.method =='POST':
		task_id = request.POST['task_id']
		task = Task.objects.get(id = task_id)
		task.delete()
	return index(request, number, jid)

@login_required(login_url='/login/')
def pay_invoice(request, number=0, jid=0):
	context_dict = summary_header(number, jid)
	if request.method =='POST':
		task_item_id = int(request.POST['item_id'])
		contractor_paid = request.POST['contractor_paid']
		contractor_paid_date = request.POST['contractor_paid_date']
		task_item = TaskItem.objects.get(id = task_item_id)
		task_item.contractor_paid = contractor_paid
		task_item.contractor_paid_date = contractor_paid_date
		task_item.save()
	return index(request, number, jid)

@login_required(login_url='/login/')
def input_quote(request, number=0, jid=0):
	context_dict = summary_header(number, jid)
	if request.method =='POST':
		task_id = int(request.POST['task_id'])
		costs_quoted = request.POST['costs_quoted']
		highest_quote = request.POST['highest_quote']
		task = Task.objects.get(id = task_id)
		task.costs_quoted = costs_quoted
		task.highest_quote = highest_quote
		task.save()
	return index(request, number, jid)


@login_required(login_url='/login/')
def delete_wishlist(request):
	context_dict = {}
	if request.method =='POST':
		item_id = request.POST['item_id']
		item = WishList.objects.get(id = item_id)
		item.delete()
	context_dict['wishlist'] = WishList.objects.all()
	return render(request, 'calc/secret.html', context_dict)

@login_required(login_url='/login/')
def allocation(request, number=0, jid=0):
	context_dict = summary_header(number, jid)
	if request.method =='POST':
		task_id = request.POST['task_id']
		task_alloc = request.POST['task_alloc']
		task = Task.objects.get(id = task_id)
		task.allocation = task_alloc
		task.save()
	return index(request, number, jid)

@login_required(login_url='/login/')
def check(request):
	context_dict = {}
	context_dict['wishlist'] = WishList.objects.all()
	context_dict['allocation'] = Task.objects.all().aggregate(Sum('allocation'))['allocation__sum']
	context_dict['profit'] = Task.objects.all().aggregate(Sum('infront_cost'))['infront_cost__sum']
	return render(request, 'calc/secret.html', context_dict)


@login_required(login_url='/login/')
def add_wishlist(request):
	context_dict = {}
	if request.method == 'POST':
		try:
			wl = WishList()
			wl.name = request.POST['name']
			wl.price = request.POST['price']
			wl.save()
		except Exception as e:
			print e
	context_dict['wishlist'] = WishList.objects.all()
	context_dict['allocation'] = Task.objects.all().aggregate(Sum('allocation'))
	context_dict['profit'] = Task.objects.all().aggregate(Sum('infront_cost'))
	return render(request, 'calc/secret.html', context_dict)


def delete_item(request, number=0, jid=0):
	if request.method =='POST':
		try:
			task_item_id = request.POST['task_item_id']
			taskItem = TaskItem.objects.get(id = task_item_id)
			task_id = taskItem.task.id
			taskItem.delete()
			update_task(task_id)
		except Exception as e:
			print e
	return index(request, number, jid)

@login_required(login_url='/login/')
def edit_task(request, number=0, jid=0):
	if request.method =='POST':
		try:
			task_id = request.POST['task_id']
			stage = request.POST['stage']
			task_number = request.POST['task_number']
			task_name = request.POST['task_name']		
			costs_estimated = request.POST['cost_estimated']
			cost_quoted = request.POST['cost_quoted']
			highest_quote = request.POST['highest_quote']
			client_charged = request.POST['client_charged']
			payment_received = request.POST['payment_received']
			payment_date = request.POST['payment_date']
			task_completed = int(request.POST['task_completed'])
			task = Task.objects.get(id = task_id)
			task.stage = stage
			task.task_number = task_number
			task.task_name = task_name
			task.costs_estimated = costs_estimated
			task.costs_quoted = cost_quoted
			task.highest_quote = highest_quote
			task.client_charged = client_charged
			task.payment_received = payment_received
			task.payment_date = payment_date
			if task_completed == 1:
				task.task_complete = False;
			else:
				task.task_complete = True;
			task.save()
			update_task(task_id)
		except Exception as e:
			print e
	return index(request, number, jid)

@login_required(login_url='/login/')
def edit_item(request, number=0, jid=0):
	if request.method =='POST':
		try:
			item_id = int(request.POST['item_id'])
			item_number = request.POST['item_number']
			item_name = request.POST['item_name']
			expense_incurred = request.POST['expense_incurred']
			invoice_number = request.POST['invoice_number']
			trade_contractor = request.POST['trade_contractor']
			contractor_paid = request.POST['contractor_paid']
			contractor_paid_date = request.POST['contractor_paid_date']
			allocation = request.POST['item_allocation']
			item = TaskItem.objects.get(id = item_id)
			item.item_number = item_number
			item.item_name = item_name	
			item.expense_incurred = expense_incurred
			item.invoice_number = invoice_number
			item.trade_contractor = trade_contractor
			item.contractor_paid = contractor_paid
			item.contractor_paid_date = contractor_paid_date
			item.allocation = allocation
			item.save()
			update_task(item.task.id)
		except Exception as e:
			print e
	return index(request, number, jid)

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user is not None:   # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/0/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("account disabled")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            context_dict={"error":"invalid login or password"}
            return render_to_response('calc/login.html', context_dict, context)
    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('calc/login.html', {}, context)


@login_required(login_url='/login/')
def restricted(request):
	context_dict={"error":"invalid login or password"}
        return render_to_response('calc/login.html', context_dict, context)
    
@login_required(login_url='/login/')
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/login/')

def summary_header(number, jid):
	context_dict = {}
	tasks = Task.objects.filter(site=number, job=jid)
	task_items = TaskItem.objects.filter(task__site=number)
	costs_estimated = tasks.aggregate(Sum('costs_estimated'))
	costs_quoted = tasks.aggregate(Sum('costs_quoted'))
	expense_incurred = tasks.aggregate(Sum('expense_incurred'))
	expense_future = tasks.aggregate(Sum('expense_future'))
	client_charged = tasks.aggregate(Sum('client_charged'))
	payment_received = tasks.aggregate(Sum('payment_received'))
	under_quote_by = tasks.aggregate(Sum('under_quote_by'))
	under_quote_by2 = tasks.aggregate(Sum('under_quote_by2'))
	expense_future_calculator = tasks.aggregate(Sum('expense_future_calculator'))
	infront_cost = tasks.aggregate(Sum('infront_cost'))
	allocations = task_items.aggregate(Sum('allocation'))
	context_dict['costs_estimated'] = costs_estimated['costs_estimated__sum']
	context_dict['costs_quoted'] = costs_quoted['costs_quoted__sum']
	context_dict['expense_incurred'] = expense_incurred['expense_incurred__sum']
	context_dict['expense_future'] = expense_future['expense_future__sum']
	context_dict['client_charged'] = client_charged['client_charged__sum']
	context_dict['payment_received'] = payment_received['payment_received__sum']
	context_dict['allocations'] = allocations['allocation__sum']
	context_dict['under_quote_by'] = under_quote_by['under_quote_by__sum']
	context_dict['under_quote_by2'] = under_quote_by2['under_quote_by2__sum']
	context_dict['expense_future_calculator'] = expense_future_calculator['expense_future_calculator__sum']
	context_dict['infront_cost'] = infront_cost['infront_cost__sum']
	return context_dict

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

def pdfView(request, number = 0, jid=0):
    #Retrieve data or whatever you need
    context_dict = {}
    context_dict['tasks']=Task.objects.filter(site=number)
    context_dict['task_items'] = TaskItem.objects.all()
    context_dict['number'] = number
    context_dict['jid'] = jid
    context_dict['pagesize'] = 'A3 landscape'
    return render_to_pdf(
            'calc/pdf.html',
            context_dict,
        )

def export_to_xls(request, number = 0, jid=0):
	tasks = Task.objects.filter(site=number, job=jid)
	task_items = TaskItem.objects.filter(task__site=number)

	# Create the HttpResponse object with Excel header.This tells browsers that 
	# the document is a Excel file.
	response = HttpResponse(content_type='application/ms-excel')

	# The response also has additional Content-Disposition header, which contains 
	# the name of the Excel file.
	response['Content-Disposition'] = 'attachment; filename=books.xls'

	# Create object for the Workbook which is under xlwt library.
	workbook = xlwt.Workbook()

	# By using Workbook object, add the sheet with the name of your choice.
	worksheet = workbook.add_sheet("Ideas")

	row_num = 0
	columns = ['Stage', 'Number', 'Description', 'Costs Estimated', 'Costs Quoted', 'Highest Quote', 'Expense Incurred', 'Invoice Number', 'Trade Contractor', 'Contractor Paid', 'Paid Date', 'Task Complete', 'Under Estimate', 'Under Quote', 'Expense Future Calculator', 'Expense Future', 'Infront Cost Estimated', 'Charged', 'Payment Received', 'Payment Date']
	for col_num in range(len(columns)):
	    # For each cell in your Excel Sheet, call write function by passing row number, 
	    # column number and cell data.
	    worksheet.write(row_num, col_num, columns[col_num])     

	for task in tasks:
	    row_num += 1
	    row = [task.stage,task.item_no,task.task_name,task.costs_estimated, task.costs_quoted, task.highest_quote, task.expense_incurred,'', '', '', '', task.task_complete, task.under_quote_by, task.under_quote_by2, task.expense_future_calculator, task.expense_future, task.infront_cost, task.client_charged, task.payment_received, str(task.payment_date)]
	    for col_num in range(len(row)):
	        worksheet.write(row_num, col_num, row[col_num])
	    for task_item in task_items:
	    	if task_item.task == task:
	    		row_num += 1
	    		cp = task_item.contractor_paid
	    		if cp == 0:
	    			cp = ''
	    			cpd = ''
	    		else:
	    			cpd = str(task_item.contractor_paid_date)
	    		row = ['', '', task_item.item_name, '', '', '', task_item.expense_incurred, task_item.invoice_no, task_item.trade_contractor, cp, cpd, '', '', '', '', '', '', '', '', '', '']
	    		for col_num in range(len(row)):
	        		worksheet.write(row_num, col_num, row[col_num])
	workbook.save(response)
	return response

