from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm
from tasks.models import Employee,Task,TaskDetails,Project
from datetime import date
from django.db.models import Q,Count

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

    """Related Data Queries [Advanced (select_related and prefetch_related)]"""
    '''(select_related) works on (ForeignKey, OneToOneField)'''
    # tasks = Task.objects.all() # Accessing TaskDetails data using reverse relationship (bad query)
    '''select_related on OneToOne'''
    # select_related on Task
    # tasks = Task.objects.select_related('details').all() # (good query)
    # select_related on TaskDetails
    # tasks = TaskDetails.objects.select_related('task').all() # (good query)
    '''select_related on ForeignKey (works only one way where foreignKey is linked)'''
    # select_related (between Task and Project)
    # tasks = Task.objects.select_related('project').all()
    '''(prefetch_related) works on (reverse ForeignKey, ManyToManyField)'''
    '''ForeignKey'''
    # between (project and task)
    # tasks = Project.objects.prefetch_related('project_task').all()
    '''ManyToManyField'''
    # between (Task and Employee)
    # prefetch_related on Task
    # tasks = Task.objects.prefetch_related('assigned_to').all()
    # prefetch_related on Employee (Reverse Relation)
    tasks = Employee.objects.prefetch_related('tasks').all()

    """Aggregate function query [Count,Avg,Max,Min,etc]"""
    # Count total task
    cnt_task = Task.objects.aggregate(total_cnt=Count('id'))
    # Count all tasks that available in a Project using (annotate)
    projects = Project.objects.annotate(task_cnt=Count('project_task'))

    return render(request, "show_task.html", {"tasks":tasks, "cnt_task":cnt_task, "projects":projects})