from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def build_profile(sender, instance, created, **kwargs):
    if created:
        age = 15
        city = "Unknown"
        position = "Unknown"
        Profile.objects.create(user=instance, age=age, city=city, position=position)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()