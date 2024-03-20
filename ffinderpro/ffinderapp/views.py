# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm, LoginForm, PlayerSignUpForm, TeamSignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Player, Profile, Team, TeamProfile

def home(request):
    return render(request, 'ffinderapp/home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Check the registration type and create the appropriate profile
            registration_type = form.cleaned_data.get('registration_type')
            if registration_type == 'player':
                player_profile = Player(user_profile=Profile.objects.create(user=user))
                player_profile.save()
            elif registration_type == 'team':
                team_profile = Team(user_profile=TeamProfile.objects.create(user=user))
                team_profile.save()

            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'ffinderapp/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'ffinderapp/login.html', {'form': form})

def player_signup(request):
    if request.method == 'POST':
        form = PlayerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('player_profile')
    else:
        form = PlayerSignUpForm()
    return render(request, 'ffinderapp/player_signup.html', {'form': form})

def team_signup(request):
    if request.method == 'POST':
        form = TeamSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('team_profile')
    else:
        form = TeamSignUpForm()
    return render(request, 'ffinderapp/team_signup.html', {'form': form})

@login_required
def profile(request):
    if request.user.is_player:
        profile, created = PlayerProfile.objects.get_or_create(user=request.user)

        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
            player_form = PlayerUpdateForm(request.POST, instance=profile)

            if u_form.is_valid() and p_form.is_valid() and player_form.is_valid():
                u_form.save()
                p_form.save()
                player_form.save()
                messages.success(request, 'Your account has been successfully updated.')
                return redirect('home')
            else:
                messages.error(request, 'Error updating your account. Please check the form.')
        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=profile)
            player_form = PlayerUpdateForm(instance=profile)

        context = {'u_form': u_form, 'p_form': p_form, 'player_form': player_form, 'title': 'profile'}
        return render(request, 'ffinderapp/player_profile.html', context)

    elif request.user.is_team:
        profile, created = TeamProfile.objects.get_or_create(user=request.user)

        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
            team_form = TeamUpdateForm(request.POST, instance=profile)

            if u_form.is_valid() and p_form.is_valid() and team_form.is_valid():
                u_form.save()
                p_form.save()
                team_form.save()
                messages.success(request, 'Your account has been successfully updated.')
                return redirect('home')
            else:
                messages.error(request, 'Error updating your account. Please check the form.')
        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=profile)
            team_form = TeamUpdateForm(instance=profile)

        context = {'u_form': u_form, 'p_form': p_form, 'team_form': team_form, 'title': 'profile'}
        return render(request, 'ffinderapp/team_profile.html', context)
    else:
        # Handle users without a specific role (e.g., basic users)
        messages.error(request, 'You need to be a player or a team to access this page.')
        return redirect('home')