# Full path and name to your csv file
csv_filepathname="/Users/assetsarsengaliyev/calculator/data-aset.csv"
# Full path to your django project directory
your_djangoproject_home="/Users/assetsarsengaliyev/calculator"


import django
django.setup()
import sys,os
sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'calculator.settings'

from calc.models import Task

import csv
dataReader = csv.reader(open(csv_filepathname), delimiter=';', quotechar='"')

for row in dataReader:
	task = Task()
	task.site = 2
	task.stage = row[0]
	task.item_no = row[1]
	task.task_name = row[2]
	task.save()

