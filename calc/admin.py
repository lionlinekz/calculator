from django.contrib import admin
from calc.models import Task, TaskItem, Idea

admin.site.register(Task)
admin.site.register(TaskItem)
admin.site.register(Idea)