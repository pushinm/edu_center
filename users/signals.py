from .models import Profile, MyUser
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=MyUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    if not created:
        instance.user_profile.save()
