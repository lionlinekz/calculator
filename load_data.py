# Full path and name to your csv file
csv_filepathname="/home/asset/calculator/data-aset.csv"
# Full path to your django project directory
your_djangoproject_home="/home/asset/calculator"


import django
django.setup()
import sys,os
sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'calculator.settings'

from calc.models import Stage

import csv
dataReader = csv.reader(open(csv_filepathname), delimiter=';', quotechar='"')

for row in dataReader:
	try:
		stage = Stage()
		stage.name = row[0]
		stage.save()
	except Exception as e:
		print e

