from django.db.models.signals import  post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from tasks.models import Task

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