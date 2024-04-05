from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    is_player = models.BooleanField(default=False)
    is_team = models.BooleanField(default=False)
    team = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True, blank=True, related_name='team_members')
    photo = models.ImageField(upload_to='media/', null=True, blank=True)




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
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='team_association')
    name = models.CharField(max_length=100)
    league = models.CharField(max_length=100)
    league_division = models.CharField(max_length=50)
    level_on_pyramid = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='team_photos/', null=True, blank=True)
    # Add more fields as needed

    def __str__(self):
        return self.name

User = get_user_model()

class Listing(models.Model):
    team = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # Assuming team is a custom user model
    title = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=100, default='') 
    city = models.CharField(max_length=100, default='')
    photo = models.ImageField(upload_to='media/listing_photos/', null=True, blank=True)  # Adding photo field
    positions = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.title

class Application(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    message = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)
    # Add more fields as needed


class PlayerProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, primary_key=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='media/player_photos/', null=True, blank=True)
    previous_clubs = models.TextField(null=True, blank=True)  # Example field
    position = models.CharField(max_length=100, null=True, blank=True)
    # Add more fields specific to player profile
    def __str__(self):
        return self.user


class TeamProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, default='') 
    league = models.CharField(max_length=100)
    league_division = models.CharField(max_length=50)
    level_on_pyramid = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='media/team_profile_photos/', default='/Users/mcolley/Developmentproject/ffinderpro/ffinderapp/static/media/logo.jpeg', null=True, blank=True)
    # Add more fields specific to team profile


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f'{self.sender} -> {self.recipient}: {self.content}'
    

class PlayerListing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    position = models.CharField(max_length=50)
    # Add more fields as needed