from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm
from tasks.models import Employee,Task

def manager_dashboard(request):
    return render(request, "dashboard/manager-dashboard.html")

def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")

def test(request):
    context = {
            'name': 'mahfuz',
            'age': 22,
            'address': 'rajshahi'
        }
    return render(request, "test.html",context)


def create_task(request):
    # employees = Employee.objects.all()
    # form = TaskForm(employees=employees) # For TaskForm
    form = TaskModelForm() # for GET Request
    if request.method == "POST":
        # form = TaskForm(request.POST, employees=employees)
        form = TaskModelForm(request.POST)
        if form.is_valid():
            '''For Django Model Form'''
            form.save()
            
            return render(request, "task_form.html", {"form": form, "message":"Task Added Successful!"})
            
    context = {"form": form}
    return render(request, "task_form.html",context)

def view_task(request):
    # retrieve all tasks data
    tasks = Task.objects.all()
    # retrieve specific single data
    task_specific = Task.objects.get(id=9)
    # retrieve first data
    task_first = Task.objects.first()
    return render(request, "show_task.html", {"tasks":tasks, "task_specific":task_specific, "task_first":task_first})