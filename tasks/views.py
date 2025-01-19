from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm
from tasks.models import Employee,Task,TaskDetails
from datetime import date
from django.db.models import Q

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
    form = TaskModelForm() # for GET Request
    if request.method == "POST":
        form = TaskModelForm(request.POST)
        if form.is_valid():
            '''For Django Model Form'''
            form.save()
            
            return render(request, "task_form.html", {"form": form, "message":"Task Added Successful!"})
            
    context = {"form": form}
    return render(request, "task_form.html",context)

def view_task(request):
    """Retrieve data from Tasks"""
    # retrieve all tasks data
    tasks = Task.objects.all()
    # retrieve specific single data
    task_specific = Task.objects.get(id=9)
    # retrieve first data
    task_first = Task.objects.first()

    """Filter data from Tasks"""
    # filter data depending on status
    pending_task = Task.objects.filter(status="PENDING")
    # show the task which due_data is Today
    due_date = Task.objects.filter(due_date=date.today())
    # show the all tasks which priority is not low
    priority = TaskDetails.objects.exclude(priority="H")
    # show the task that contains specific word example: around
    task_by_text = Task.objects.filter(title__icontains="around")
    # show the task that contains specific word example: it and status: completed
    task_by_text = Task.objects.filter(title__icontains="it", status="COMPLETED")
    # show the tasks which status pending or completed
    status = Task.objects.filter(Q(status="PENDING") | Q(status="COMPLETED"))
    # to check data available or not
    check = Task.objects.filter(status="PENDING").exists()

    return render(request, "show_task.html", {"pending_task":pending_task, "due_date":due_date, "priority":priority,
                                              "task_by_text":task_by_text, "status":status, "check":check
                                              })