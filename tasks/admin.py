from django.contrib import admin
from tasks.models import Task, TaskDetails, Employee, Project

# Register your models here.
admin.site.register(Task)
admin.site.register(TaskDetails)
admin.site.register(Employee)
admin.site.register(Project)