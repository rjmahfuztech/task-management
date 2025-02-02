from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm,TaskDetailsModelForm
from tasks.models import Task,TaskDetails,Project
from datetime import date, timedelta 
from django.db.models import Q,Count
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required

# Test for manager
def is_manager(user):
    return user.groups.filter(name='Admin').exists()
#Test for employee
def is_employee(user):
    return user.groups.filter(name='Admin').exists()


@user_passes_test(is_manager, login_url='no-permission')
def manager_dashboard(request):
    # tasks = Task.objects.all() Not optimized query
    base_query = Task.objects.select_related('details').prefetch_related('assigned_to') # optimized query
    type = request.GET.get('type', 'all')

    # Retrieving data from dataBase depending on condition
    if type == 'completed':
        tasks = base_query.filter(status='COMPLETED')
    elif type == 'in_progress':
        tasks = base_query.filter(status='IN_PROGRESS')
    elif type == 'pending':
        tasks = base_query.filter(status='PENDING')
    else:
        tasks = base_query.all()

    # getting tasks count without optimized query
    # total_task = tasks.count()
    # completed_task = Task.objects.filter(status="COMPLETED").count()
    # in_progress_task = Task.objects.filter(status="IN_PROGRESS").count()
    # pending_task = Task.objects.filter(status="PENDING").count()

    # optimized counting query
    counts = Task.objects.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(status='COMPLETED')),
        in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
        pending=Count('id', filter=Q(status='PENDING'))
    )

    context = {
        'tasks': tasks,
        'counts': counts
    }
    return render(request, "dashboard/manager-dashboard.html",context)

@user_passes_test(is_employee, login_url='no-permission')
def employee_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")

@login_required
@permission_required('tasks.add_task', login_url='no-permission')
def create_task(request):
    task_form = TaskModelForm() # for GET Request
    task_details_form = TaskDetailsModelForm()
    
    if request.method == "POST":
        task_form = TaskModelForm(request.POST)
        task_details_form = TaskDetailsModelForm(request.POST, request.FILES)

        if task_form.is_valid() and task_details_form.is_valid():
            '''For Django Model Form'''
            task = task_form.save()
            task_details = task_details_form.save(commit=False)
            task_details.task = task
            task_details.save()
            
            messages.success(request, "Task Created Successful!!")
            return redirect('create-task')
            
    context = {"task_form": task_form, "task_details_form":task_details_form}
    return render(request, "task_form.html",context)


@login_required
@permission_required('tasks.change_task', login_url='no-permission')
def update_task(request, id):
    task = Task.objects.get(id=id) # getting specific id for update
    task_form = TaskModelForm(instance=task)
    if task.details:
        task_details_form = TaskDetailsModelForm(instance=task.details)
    
    if request.method == "POST":
        task_form = TaskModelForm(request.POST, instance=task)
        task_details_form = TaskDetailsModelForm(request.POST, instance=task.details)

        if task_form.is_valid() and task_details_form.is_valid():
            task = task_form.save()
            task_details = task_details_form.save(commit=False)
            task_details.task = task
            task_details.save()
            
            messages.success(request, "Task Updated Successful!!")
            return redirect('update-task', id)
            
    context = {"task_form": task_form, "task_details_form":task_details_form}
    return render(request, "task_form.html",context)


@login_required
@permission_required('tasks.delete_task', login_url='no-permission')
def delete_task(request, id):
    task = Task.objects.get(id=id)
    if request.method == "POST":
        task.delete()
        messages.success(request, "Task Deleted Successful!!")
        return redirect('manager-dashboard')
    else:
        messages.error(request, "Something Went Wrong!!! Please Try again!")
        return redirect('manager-dashboard')

@login_required
@permission_required('tasks.view_task', login_url='no-permission')
def view_task(request):
    """Retrieve data from Tasks"""
    # retrieve all tasks data
    # tasks = Task.objects.all()
    # retrieve specific single data
    task_specific = Task.objects.get(id=9)
    # retrieve first data
    task_first = Task.objects.first()

    """Filter data from Tasks"""
    # filter data depending on status
    # pending_task = Task.objects.filter(status="PENDING")
    # show the task which due_data is Today
    # due_date = Task.objects.filter(due_date=date.today())
    # show the all tasks which priority is not low
    # priority = TaskDetails.objects.exclude(priority="H")
    # show the task that contains specific word example: around
    # task_by_text = Task.objects.filter(title__icontains="around")
    # show the task that contains specific word example: it and status: completed
    # task_by_text = Task.objects.filter(title__icontains="it", status="COMPLETED")
    # show the tasks which status pending or completed
    # status = Task.objects.filter(Q(status="PENDING") | Q(status="COMPLETED"))
    # to check data available or not
    # check = Task.objects.filter(status="PENDING").exists()

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
    tasks = Task.objects.prefetch_related('assigned_to').all()
    # prefetch_related on Employee (Reverse Relation)
    # tasks = Employee.objects.prefetch_related('tasks').all()

    """Aggregate function query [Count,Avg,Max,Min,etc]"""
    # Count total task
    cnt_task = Task.objects.aggregate(total_cnt=Count('id'))
    # Count all tasks that available in a Project using (annotate)
    projects = Project.objects.annotate(task_cnt=Count('project_task'))

    return render(request, "show_task.html", {"tasks":tasks, "cnt_task":cnt_task, "projects":projects})


def task_details(request, task_id):
    task = Task.objects.select_related('details').get(id=task_id)
    status_choices = Task.STATUS_CHOICES
    if request.method == 'POST':
        change_status = request.POST.get('task_status')
        task.status = change_status
        task.save()

    return render(request, "task_details.html", {"task": task, "status_choices": status_choices})
