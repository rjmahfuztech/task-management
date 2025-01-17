from django.db import models

# Create your models here.
# many to many
class Employee(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    # task_set

class Task(models.Model):
    project = models.ForeignKey("Project",
        on_delete=models.CASCADE,
        default=1,
        related_name='project_task'
    )
    # employee table
    assigned_to = models.ManyToManyField(Employee, related_name='tasks')
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # taskdetails


# one to one
class TaskDetails(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    PRIORITY_OPTIONS = (
            (HIGH, 'High'),
            (MEDIUM, 'Medium'),
            (LOW, 'Low')
        )
    task = models.OneToOneField(
        Task,
        on_delete=models.CASCADE,
        related_name='details'
    )
    assigned_to = models.CharField(max_length=100)
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default=LOW)

# Task.objects.get(id=2)
# select * from Task where id = 2
# ORM = Object Relational Mapper

# one to many
class Project(models.Model):
    name = models.CharField(max_length=150)
    start_date = models.DateField()
    # task