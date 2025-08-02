# signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Task

@receiver(pre_save, sender=Task)
def notify_status_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # Новая задача — не уведомляем

    old_task = Task.objects.get(pk=instance.pk)
    if old_task.status != instance.status:
        subject = f"Task status is changed: {instance.title}"
        message = f"Task '{instance.title}' has now status: {instance.get_status_display()}"
        send_mail(subject, message, None, [instance.owner.email])