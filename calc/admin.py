from django.contrib import admin
from calc.models import Task, TaskItem, Idea, Job

admin.site.register(Task)
admin.site.register(TaskItem)
admin.site.register(Idea)
admin.site.register(Job)