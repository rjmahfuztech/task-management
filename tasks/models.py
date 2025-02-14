from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Task(models.Model):
    PENDING = 'PENDING'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    STATUS_CHOICES = [
            (PENDING, 'Pending'),
            (IN_PROGRESS, 'In Progress'),
            (COMPLETED, 'Completed')
        ]
    project = models.ForeignKey("Project",
        on_delete=models.CASCADE,
        default=1,
        related_name='project_task'
    )
    assigned_to = models.ManyToManyField(User, related_name='tasks')
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


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
        on_delete=models.DO_NOTHING,
        related_name='details'
    )
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default=LOW)
    notes = models.TextField(blank=True, null=True)
    asset = models.ImageField(upload_to='tasks_asset', blank=True, null=True, default='tasks_asset/default-img.jpg')

    def __str__(self):
        return f"Details from Task {self.task.title}"


class Project(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(blank=True, null=True)
    start_date = models.DateField()

    def __str__(self):
        return self.name
    