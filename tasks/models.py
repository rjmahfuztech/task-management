from django.db import models
from django.db.models.signals import  post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail

class Employee(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

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
    assigned_to = models.ManyToManyField(Employee, related_name='tasks')
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    is_completed = models.BooleanField(default=False)
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
    # assigned_to = models.CharField(max_length=100)
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default=LOW)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Details from Task {self.task.title}"


class Project(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(blank=True, null=True)
    start_date = models.DateField()

    def __str__(self):
        return self.name
    

"""Django Signals"""

# @receiver(pre_save, sender=Task)
# def notify_task_creation(sender, instance, **kwargs):
#     print('sender', sender)
#     print('instance', instance)
#     print('kwargs', kwargs)
#     instance.is_completed = True

@receiver(m2m_changed, sender=Task.assigned_to.through)
def notify_employee_on_task_creation(sender, instance, action, **kwargs):
    if action == 'post_add':
        assigned_email = [emp.email for emp in instance.assigned_to.all()]
        
        send_mail(
            "New Task Assigned",
            f"You have been assigned to the task: {instance.title}",
            "codrmahfuz@gmail.com",
            assigned_email,
        )


@receiver(post_delete, sender=Task)
def delete_associated_details(sender, instance, **kwargs):
    if instance.details:
        print(instance)
        instance.details.delete()
        print("deleted successful!")
    
