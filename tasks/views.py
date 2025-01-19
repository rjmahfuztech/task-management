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

            """For Django Form"""
            # data = form.cleaned_data
            # title = data.get('title')
            # description = data.get('description')
            # due_date = data.get('due_date')
            # assigned_to = data.get('assigned_to')
            
            # task = Task.objects.create(title=title, description=description, due_date=due_date)
            # for emp_id in assigned_to:
            #     employee = Employee.objects.get(id=emp_id)
            #     task.assigned_to.add(employee)
            
            # return HttpResponse("Task Added Successful!")
            
    context = {"form": form}
    return render(request, "task_form.html",context)