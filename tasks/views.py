from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskForm,TaskModelForm,TaskDetailsModelForm
from tasks.models import Task,TaskDetails,Project
from datetime import date, timedelta 
from django.db.models import Q,Count
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from users.views import is_admin
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import ContextMixin
from django.views.generic import ListView, DetailView,UpdateView, TemplateView, DeleteView
from django.urls import reverse_lazy

# Test for manager
def is_manager(user):
    return user.groups.filter(name='Manager').exists()
#Test for employee
def is_employee(user):
    return user.groups.filter(name='User').exists()


# Manager dashboard view
manager_decorators = [login_required, user_passes_test(is_manager, login_url='no-permission')]
@method_decorator(manager_decorators, name='dispatch')
class ManagerDashboardView(ListView):
    model = Task
    template_name = 'dashboard/manager-dashboard.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        base_query = Task.objects.select_related('details').prefetch_related('assigned_to')
        type = self.request.GET.get('type', 'all')

        if type == 'completed':
            queryset = base_query.filter(status='COMPLETED')
        elif type == 'in_progress':
            queryset = base_query.filter(status='IN_PROGRESS')
        elif type == 'pending':
            queryset = base_query.filter(status='PENDING')
        else:
            queryset = base_query.all()
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        counts = Task.objects.aggregate(
            total=Count('id'),
            completed=Count('id', filter=Q(status='COMPLETED')),
            in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
            pending=Count('id', filter=Q(status='PENDING'))
        )
        context["counts"] = counts
        return context
    

# Employee dashboard view
employee_decorators = [login_required, user_passes_test(is_employee, login_url='no-permission')]
@method_decorator(employee_decorators, name='dispatch')
class EmployeeDashboardView(TemplateView):
    template_name = 'dashboard/user-dashboard.html'


""" Class Base View for create_task """

# create_decorators = [login_required, permission_required('tasks.add_task', login_url='no-permission')]
# @method_decorator(create_decorators, name="dispatch")
class CreateTask(LoginRequiredMixin,PermissionRequiredMixin, ContextMixin, View):
    # for mixin authentication
    permission_required = 'tasks.add_task'
    login_url = 'sign-in'
    template_name = "task_form.html"

    # context mixin
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = kwargs.get('task_form', TaskModelForm())
        context['task_details_form'] = kwargs.get('task_details_form', TaskDetailsModelForm())
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    
    def post(self, request, *args, **kwargs):
        task_form = TaskModelForm(request.POST)
        task_details_form = TaskDetailsModelForm(request.POST, request.FILES)

        if task_form.is_valid() and task_details_form.is_valid():
            '''For Django Model Form'''
            task = task_form.save()
            task_details = task_details_form.save(commit=False)
            task_details.task = task
            task_details.save()
            
            messages.success(request, "Task Created Successful!!")
            # return redirect('create-task')
            context = self.get_context_data(task_form=task_form, task_details_form=task_details_form)
            return render(request, self.template_name, context)


""" Class Base View for create_task """
update_task_decorators = [login_required, permission_required('tasks.change_task', login_url='no-permission')]
@method_decorator(update_task_decorators, name="dispatch")
class UpdateTask(UpdateView):
    model = Task
    form_class = TaskModelForm
    context_object_name = 'task'
    template_name = 'task_form.html'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = self.get_form()

        if hasattr(self.object, 'details') and self.object.details:
            context['task_details_form'] = TaskDetailsModelForm(instance=self.object.details)
        else:
            context['task_details_form'] = TaskDetailsModelForm()

        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        task_form = TaskModelForm(request.POST, instance=self.object)
        task_details_form = TaskDetailsModelForm(request.POST, request.FILES, instance=getattr(self.object, 'details', None))

        if task_form.is_valid() and task_details_form.is_valid():
            task = task_form.save()
            task_details = task_details_form.save(commit=False)
            task_details.task = task
            task_details.save()

            messages.success(request, "Task Updated Successful!!")
            return redirect('update-task', self.object.id)
        
        return redirect('update-task', self.object.id)

    
# Delete task view
delete_task_decorators = [login_required, permission_required('tasks.delete_task', login_url='no-permission')]
@method_decorator(delete_task_decorators, name="dispatch")
class DeleteTaskView(DeleteView):
    model = Task
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('manager-dashboard')

    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            self.object.delete()
            messages.success(request, "Task Deleted Successful!!")
            return redirect(self.success_url)
        except Exception:
            messages.error(request, "Something Went Wrong!!! Please Try again!")
            return redirect('manager-dashboard')


""" Class Base View for ViewProject """
view_project_decorators = [login_required, permission_required('tasks.view_project', login_url='no-permission')]
@method_decorator(view_project_decorators, name="dispatch")
class ViewProject(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'show_task.html'

    def get_queryset(self):
        queryset = Project.objects.annotate(task_cnt=Count('project_task'))
        return queryset


""" Class Base View for TaskDetails """
class TaskDetails(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'task_details.html'
    pk_url_kwarg = 'task_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Task.STATUS_CHOICES
        return context
    
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        change_status = request.POST.get('task_status')
        task.status = change_status
        task.save()
        return redirect('task-details', task.id)

@login_required
def dashboard(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_manager(request.user):
        return redirect('manager-dashboard')
    elif is_employee(request.user):
        return redirect('user-dashboard')
    
    return redirect('no-permission')