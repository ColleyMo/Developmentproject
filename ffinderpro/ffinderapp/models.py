from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return self.user.username

class Player(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    position = models.CharField(max_length=50)  # Choose an appropriate max_length
    date_of_birth = models.DateField()
    previous_clubs = models.TextField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)

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
