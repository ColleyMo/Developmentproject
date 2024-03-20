# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Player, Team

class SignUpForm(UserCreationForm):
    USER_CHOICES = (
        ('player', 'Player'),
        ('team', 'Team'),
    )
    registration_type = forms.ChoiceField(choices=USER_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    class Meta:
        model = User

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.widgets.DateInput(attrs={'type': 'date'}),
        help_text='Enter your date of birth'
    )

    class Meta:
        model = Player  # Assuming Player is the profile model for players
        fields = ['date_of_birth', 'address', 'city', 'photo']

class PlayerSignUpForm(UserCreationForm):
    class Meta:
        model = Player
        fields = ['date_of_birth', 'previous_clubs', 'address', 'city', 'photo']

    def __init__(self, *args, **kwargs):
        super(PlayerSignUpForm, self).__init__(*args, **kwargs)
        # Remove the 'username' field from the form
        del self.fields['username']

class TeamSignUpForm(UserCreationForm):
    class Meta:
        model = Team
        fields = ['name', 'location', 'league', 'league_division', 'level_on_pyramid']

    def __init__(self, *args, **kwargs):
        super(TeamSignUpForm, self).__init__(*args, **kwargs)
        # Remove the 'username' field from the form
        del self.fields['username']
