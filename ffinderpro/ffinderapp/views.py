from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm

def home(request):
    return render(request, 'ffinderapp/home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
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


@login_required
def profile(request):
    # Try to get the user's profile, or create it if it doesn't exist
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been successfully updated.')
            return redirect('home')
        else:
            messages.error(request, 'Error updating your account. Please check the form.')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {'u_form': u_form, 'p_form': p_form, 'title': 'profile'}
    return render(request, 'ffinderapp/profile.html', context)