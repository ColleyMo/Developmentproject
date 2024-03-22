from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    is_player = models.BooleanField(default=False)
    is_team = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Custom users"

# Resolve clash by specifying unique related names for groups and user_permissions fields
CustomUser._meta.get_field('groups').remote_field.related_name = 'custom_user_groups'
CustomUser._meta.get_field('user_permissions').remote_field.related_name = 'custom_user_permissions'

class Player(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='player_photos/', null=True, blank=True)
    # Add more fields as needed


class Team(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    league = models.CharField(max_length=100)
    league_division = models.CharField(max_length=50)
    level_on_pyramid = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='team_photos/', null=True, blank=True)
    # Add more fields as needed

User = get_user_model()

class Listing(models.Model):
    team = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # Assuming team is a custom user model
    title = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=100)  # Adding location field
    photo = models.ImageField(upload_to='listing_photos/', null=True, blank=True)  # Adding photo field
    positions = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Application(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    message = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)
    # Add more fields as needed


class PlayerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='player_photos/', null=True, blank=True)
    # Add more fields specific to player profile


class TeamProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    league = models.CharField(max_length=100)
    league_division = models.CharField(max_length=50)
    level_on_pyramid = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='team_profile_photos/', default='/Users/mcolley/Developmentproject/ffinderpro/ffinderapp/static/media/logo.jpeg', null=True, blank=True)
    # Add more fields specific to team profile