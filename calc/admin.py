from django.contrib import admin
from calc.models import Task, TaskItem, Idea, Job, Stage, Invoice, Payment

admin.site.register(Task)
admin.site.register(TaskItem)
admin.site.register(Idea)
admin.site.register(Job)
admin.site.register(Stage)
admin.site.register(Invoice)
admin.site.register(Payment)