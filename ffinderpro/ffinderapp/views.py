from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, PlayerSignUpForm, TeamSignUpForm, ListingForm, ProfileUpdateForm, PlayerProfileForm, TeamProfileForm
from .models import CustomUser, Player, PlayerProfile, TeamProfile, Listing


def home(request):
    return render(request, 'ffinderapp/home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Create a new CustomUser instance (assuming you have a CustomUser model)
            custom_user = form.save()
            registration_type = form.cleaned_data.get('registration_type')
            if registration_type == 'player':
                # Create a new Player profile instance and associate it with the CustomUser
                player_profile = Player(user_profile=custom_user.profile)
                player_profile.save()
            elif registration_type == 'team':
                # Create a new TeamProfile instance and associate it with the CustomUser
                team_profile = TeamProfile(user=custom_user.profile, **form.cleaned_data)
                team_profile.save()
            login(request, custom_user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'ffinderapp/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'ffinderapp/login.html', {'form': form})


def player_signup(request):
    if request.method == 'POST':
        form = PlayerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            player_profile = PlayerProfile.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = PlayerSignUpForm()
    return render(request, 'ffinderapp/player_signup.html', {'form': form})


def team_signup(request):
    if request.method == 'POST':
        form = TeamSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            team_profile = TeamProfile.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = TeamSignUpForm()
    return render(request, 'ffinderapp/team_signup.html', {'form': form})


def profile(request):
    u_form = None  # Initialize u_form to None
    p_form = None  # Initialize p_form to None
    t_form = None  # Initialize t_form to None

    if hasattr(request.user, 'playerprofile'):
        player_profile = request.user.playerprofile
        if request.method == 'POST':
            u_form = ProfileUpdateForm(request.POST, instance=request.user)
            p_form = PlayerProfileForm(request.POST, request.FILES, instance=player_profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, 'Your profile has been updated!')
                return redirect('profile')
        else:
            u_form = ProfileUpdateForm(instance=request.user)
            p_form = PlayerProfileForm(instance=player_profile)
    elif hasattr(request.user, 'teamprofile'):
        team_profile = request.user.teamprofile
        if request.method == 'POST':
            u_form = ProfileUpdateForm(request.POST, instance=request.user)
            t_form = TeamProfileForm(request.POST, request.FILES, instance=team_profile)
            if u_form.is_valid() and t_form.is_valid():
                u_form.save()
                t_form.save()
                messages.success(request, 'Your profile has been updated!')
                return redirect('profile')
        else:
            u_form = ProfileUpdateForm(instance=request.user)
            t_form = TeamProfileForm(instance=team_profile)
    else:
        # Handle users without a specific role
        pass  # Implement your logic here

    return render(request, 'ffinderapp/profile.html', {'u_form': u_form, 'p_form': p_form, 't_form': t_form})

def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.team = request.user
            listing.save()
            return redirect('listing_detail', listing_id=listing.id)
    else:
        form = ListingForm()
    return render(request, 'ffinderapp/create_listing.html', {'form': form})

def listing_detail(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    return render(request, 'ffinderapp/listing_detail.html', {'listing': listing})