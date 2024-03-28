from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, PlayerProfile, TeamProfile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile = Profile.objects.create(user=instance)
        PlayerProfile.objects.create(user=instance)
        TeamProfile.objects.create(user=instance)


@receiver(post_save, sender=TeamProfile)
def assign_team_role(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        user.is_team = True
        user.save()

@receiver(post_save, sender=PlayerProfile)
def assign_player_role(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        user.is_player = True
        user.save()