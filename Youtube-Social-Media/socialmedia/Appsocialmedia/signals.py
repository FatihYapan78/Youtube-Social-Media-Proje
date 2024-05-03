from django.contrib.auth.models import User
from .models import *
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created,**kwargs):
    if created:
        Profil.objects.create(user=instance)

@receiver(post_save, sender=Comment)
def comment_count_add(sender, instance, created,**kwargs):
    if created:
        instance.post.comment_count += 1
        instance.post.save()

@receiver(post_delete, sender=Comment)
def comment_count_delete(sender, instance, **kwargs):
    instance.post.comment_count -= 1
    instance.post.save()