from django.urls import path
from tasks.views import dashboard, CreateTask,ViewProject, TaskDetails, UpdateTask, EmployeeDashboardView,ManagerDashboardView,DeleteTaskView

urlpatterns = [
    path('manager-dashboard/', ManagerDashboardView.as_view(), name='manager-dashboard'),
    path('user-dashboard/', EmployeeDashboardView.as_view(), name='user-dashboard'),
    path('create-task/', CreateTask.as_view(), name='create-task'),
    path('view-project/', ViewProject.as_view(), name='view-project'),
    path('task/<int:task_id>/details/', TaskDetails.as_view(), name='task-details'),
    path('update-task/<int:id>/', UpdateTask.as_view(), name='update-task'),
    path('delete-task/<int:id>/', DeleteTaskView.as_view(), name='delete-task'),
    path('dashboard/', dashboard, name='dashboard')
]