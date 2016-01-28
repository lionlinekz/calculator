# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from calc.models import Task
from calc.models import TaskItem, Idea
from calc.models import Contract, WishList, Job
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
	context_dict = summary_header(number)
	context_dict['tasks'] = Task.objects.filter(site=number)
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

@login_required(login_url='/login/')
def view_items(request, number=0, jid=0):
	context_dict = summary_header(number)
	if request.method =='POST':
		task_id = request.POST['task_id']
		context_dict['tasks'] = Task.objects.filter(id = task_id)
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




@login_required(login_url='/login/')
def index(request, number=0, jid=0):
	context_dict = summary_header(number)
	tasks = Task.objects.filter(site=number)
	task_items = TaskItem.objects.filter(task__site=number).order_by('item_name')
	context_dict['tasks'] = tasks
	context_dict['task_items'] = task_items
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
	return render(request, 'calc/index.html', context_dict)


@login_required(login_url='/login/')
def estimate(request, number=0, jid=0):
	context_dict = summary_header(number)
	tasks = Task.objects.filter(site=number)
	task_items = TaskItem.objects.all()
	context_dict['tasks'] = tasks
	context_dict['task_items'] = task_items
	context_dict['number'] = number
	context_dict['jid'] = jid
	context_dict.update(summary_header(number))
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
	if request.method =='POST':
		price = request.POST['contract_price']
		job = Job.objects.get(pk=jid)
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
			context_dict['profit_actual'] = int(Contract.price) - expense_incurred['expense_incurred__sum']
			context_dict['profit_potential'] = int(Contract.price) - costs_quoted['costs_quoted__sum']
			context_dict['profit_estimate'] = int(Contract.price) - costs_estimated['costs_estimated__sum']
		except Exception as e:
			print e
		context_dict['jid'] = jid
	return render(request, 'calc/summary.html', context_dict)


@login_required(login_url='/login/')
def add_task(request, number=0, jid=0):
	context_dict = summary_header(number)
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
	context_dict['tasks']=Task.objects.filter(site=number)
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
	return render(request, 'calc/index.html', context_dict)

@login_required(login_url='/login/')
def add_item(request, number=0, jid=0):
	context_dict = summary_header(number)
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
	context_dict['tasks']=Task.objects.filter(site=number)
	context_dict['task_items'] = TaskItem.objects.all()
	context_dict['number'] = number
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
	context_dict = summary_header(number)
	if request.method =='POST':
		task_id = request.POST['task_id']
		task = Task.objects.get(id = task_id)
		task.delete()
	context_dict['tasks']=Task.objects.filter(site=number)
	context_dict['task_items'] = TaskItem.objects.all()
	context_dict['number'] = number
	return_html(request, context_dict)
	return index(request, number)

@login_required(login_url='/login/')
def pay_invoice(request, number=0, jid=0):
	context_dict = summary_header(number)
	if request.method =='POST':
		task_item_id = int(request.POST['item_id'])
		contractor_paid = request.POST['contractor_paid']
		contractor_paid_date = request.POST['contractor_paid_date']
		task_item = TaskItem.objects.get(id = task_item_id)
		task_item.contractor_paid = contractor_paid
		task_item.contractor_paid_date = contractor_paid_date
		task_item.save()
	context_dict['tasks']=Task.objects.filter(site=number)
	context_dict['task_items'] = TaskItem.objects.all()
	context_dict['number'] = number
	context_dict['jid'] = jid
	return_html(request, context_dict)
	return index(request, number)

@login_required(login_url='/login/')
def input_quote(request, number=0, jid=0):
	context_dict = summary_header(number)
	if request.method =='POST':
		task_id = int(request.POST['task_id'])
		costs_quoted = request.POST['costs_quoted']
		highest_quote = request.POST['highest_quote']
		task = Task.objects.get(id = task_id)
		task.costs_quoted = costs_quoted
		task.highest_quote = highest_quote
		task.save()
	context_dict['tasks']=Task.objects.filter(site=number)
	context_dict['task_items'] = TaskItem.objects.all()
	context_dict['number'] = number
	context_dict['jid'] = jid
	return_html(request, context_dict)
	return index(request, number)


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
	context_dict = summary_header(number)
	if request.method =='POST':
		task_id = request.POST['task_id']
		task_alloc = request.POST['task_alloc']
		task = Task.objects.get(id = task_id)
		task.allocation = task_alloc
		task.save()
	context_dict['tasks']=Task.objects.filter(site=number)
	context_dict['task_items'] = TaskItem.objects.all()
	context_dict['number'] = number
	context_dict['jid'] = jid
	return_html(request, context_dict)
	return index(request, number)

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
	context_dict = {}
	if request.method =='POST':
		try:
			task_item_id = request.POST['task_item_id']
			taskItem = TaskItem.objects.get(id = task_item_id)
			taskItem.delete()
		except Exception as e:
			print e
	context_dict['tasks']=Task.objects.filter(site=number)
	context_dict['task_items'] = TaskItem.objects.all()
	context_dict['number'] = number
	context_dict['jid'] = jid
	return_html(request, context_dict)
	return render(request, 'calc/index.html', context_dict)

@login_required(login_url='/login/')
def edit_task(request, number=0, jid=0):
	context_dict = summary_header(number)
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
	context_dict['tasks']=Task.objects.filter(site=number)
	context_dict['task_items'] = TaskItem.objects.all()
	context_dict['number'] = number
	context_dict['jid'] = jid
	return_html(request, context_dict)
	return render(request, 'calc/index.html', context_dict)

@login_required(login_url='/login/')
def edit_item(request, number=0, jid=0):
	context_dict = summary_header(number)
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
	context_dict['tasks']=Task.objects.filter(site=number)
	context_dict['task_items'] = TaskItem.objects.all()
	context_dict['number'] = number
	context_dict['jid'] = jid
	return_html(request, context_dict)
	return render(request, 'calc/index.html', context_dict)

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
    return HttpResponseRedirect('/0/')

def summary_header(number):
	context_dict = {}
	tasks = Task.objects.filter(site=number)
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


