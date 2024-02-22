from django.contrib.auth.models import User, Group
from django.shortcuts import render
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

from django.db import models

class NestedChoices(models.TextChoices):
    CENTER_BACK = 'cb', 'Center Back'
    RIGHT_BACK = 'rb', 'Right Back'
    LEFT_BACK = 'lb', 'Left Back'
    DEFENSIVE_MIDFIELDER = 'dm', 'Defensive Midfielder'
    CENTRAL_MIDFIELDER = 'cm', 'Central Midfielder'
    ATTACKING_MIDFIELDER = 'am', 'Attacking Midfielder'
    STRIKER = 'st', 'Striker'
    LEFT_WINGER = 'lw','Left Winger'
    RIGHT_WINGER = 'rw', 'Right Winger'


class Player(models.Model):
    POSITION_CHOICES = [
        ('gk', 'Goalkeeper'),
        ('def', [
            (NestedChoices.CENTER_BACK, 'Center Back'),
            (NestedChoices.RIGHT_BACK, 'Right Back'),
            (NestedChoices.LEFT_BACK, 'Left Back'),
        ]),
        ('mid', [
            (NestedChoices.DEFENSIVE_MIDFIELDER, 'Defensive Midfielder'),
            (NestedChoices.CENTRAL_MIDFIELDER, 'Central Midfielder'),
            (NestedChoices.ATTACKING_MIDFIELDER, 'Attacking Midfielder'),
        ]),
        ('att', [
            (NestedChoices.STRIKER, 'Striker'),
            (NestedChoices.RIGHT_WINGER, 'Right Winger'),
            (NestedChoices.LEFT_WINGER, 'Left winger'),
        ]),
    ]

    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    position = models.CharField(max_length=3, choices=POSITION_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    previous_clubs = models.TextField()
    address = models.CharField(max_length=255, default='', blank=True)
    city = models.CharField(max_length=100, default='', blank=True)
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

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    