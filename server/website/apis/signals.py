from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import StudentProxy, Student, InstructorProxy, Instructor


@receiver(post_save, sender=StudentProxy)
def save_student_receiver(sender, instance, created, **kwargs):
    if created and instance.role == "STUDENT":
        Student.objects.create(user=instance)


@receiver(post_save, sender=InstructorProxy)
def save_instructor_receiver(sender, instance, created, **kwargs):
    if created and instance.role == "INSTRUCTOR":
        Instructor.objects.create(user=instance)
