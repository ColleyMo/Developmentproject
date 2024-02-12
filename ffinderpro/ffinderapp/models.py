from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add additional fields for user profile (e.g., age, location, etc.)

    def __str__(self):
        return self.user.username

class Player(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    position = models.CharField(max_length=50)  # Choose an appropriate max_length
    age = models.IntegerField()
    previous_clubs = models.TextField()
    # Add more fields as needed

    def __str__(self):
        return self.user_profile.user.username

class Team(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    league = models.CharField(max_length=100)
    league_division = models.CharField(max_length=50)
    level_on_pyramid = models.CharField(max_length=50)
    # Add more fields as needed

    def __str__(self):
        return self.name
