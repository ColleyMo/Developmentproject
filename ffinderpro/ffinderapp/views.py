from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SignUpForm, PlayerSignUpForm, TeamSignUpForm, ListingForm, ProfileUpdateForm, PlayerProfileForm, TeamProfileForm
from .models import CustomUser, Player, PlayerProfile, TeamProfile, Listing
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
#from .models import Message
from django.http import HttpResponse
from django.views.generic import View
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


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
                player_profile = Player(user=custom_user)
                player_profile.save()
            elif registration_type == 'team':
                # Create a new TeamProfile instance and associate it with the CustomUser
                team_profile = TeamProfile(user=custom_user, **form.cleaned_data)
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

@login_required
def profile(request):
    user = request.user
    u_form = ProfileUpdateForm(instance=user)
    p_form = None
    t_form = None

    if request.method == 'POST':
        if 'player_profile_submit' in request.POST:
            p_form = PlayerProfileForm(request.POST, request.FILES)
            if p_form.is_valid():
                player_profile = p_form.save(commit=False)
                player_profile.user = user
                player_profile.save()
                messages.success(request, 'Your player profile has been created!')
                return redirect('profile')
        elif 'team_profile_submit' in request.POST:
            t_form = TeamProfileForm(request.POST, request.FILES)
            if t_form.is_valid():
                team_profile = t_form.save(commit=False)
                team_profile.user = user
                team_profile.save()
                messages.success(request, 'Your team profile has been created!')
                return redirect('profile')
    else:
        if hasattr(user, 'playerprofile'):
            player_profile = user.playerprofile
            p_form = PlayerProfileForm(instance=player_profile)
        else:
            p_form = PlayerProfileForm()

        if hasattr(user, 'teamprofile'):
            team_profile = user.teamprofile
            t_form = TeamProfileForm(instance=team_profile)
        else:
            t_form = TeamProfileForm()

    return render(request, 'ffinderapp/profile.html', {'u_form': u_form, 'p_form': p_form, 't_form': t_form, 'user': user})
    
def player_profile(request):
    user = request.user
    u_form = ProfileUpdateForm(instance=user)
    p_form = None

    if hasattr(user, 'playerprofile'):
        player_profile = user.playerprofile
        p_form = PlayerProfileForm(instance=player_profile)
    elif request.method == 'POST':
        p_form = PlayerProfileForm(request.POST, request.FILES)
        if p_form.is_valid():
            player_profile = p_form.save(commit=False)
            player_profile.user = user
            player_profile.save()
            messages.success(request, 'Your player profile has been created!')
            return redirect('player_profile')
    else:
        p_form = PlayerProfileForm()

    return render(request, 'ffinderapp/playerprofile.html', {'u_form': u_form, 'p_form': p_form})

def team_profile(request):
    user = request.user
    u_form = ProfileUpdateForm(instance=user)
    t_form = None

    if isinstance(user, get_user_model()):  # Ensure user is CustomUser instance
        if hasattr(user, 'teamprofile'):
            team_profile = user.teamprofile
            t_form = TeamProfileForm(instance=team_profile)
        elif request.method == 'POST':
            t_form = TeamProfileForm(request.POST, request.FILES)
            if t_form.is_valid():
                team_profile = t_form.save(commit=False)
                # Ensure that user is an instance of CustomUser
                if isinstance(user, get_user_model()):
                    team_profile.user = user
                    team_profile.save()
                    messages.success(request, 'Your team profile has been created!')
                    return redirect('team_profile')
                else:
                    # Handle the case where user is not an instance of CustomUser
                    # This could be due to authentication issues or misconfiguration
                    # You can log an error, redirect the user, or handle it differently based on your application's requirements
                    pass
        else:
            t_form = TeamProfileForm()
    else:
        # Handle the case where user is not a CustomUser instance
        # This could be due to authentication issues or misconfiguration
        # You can log an error, redirect the user, or handle it differently based on your application's requirements
        pass

    return render(request, 'ffinderapp/teamprofile.html', {'u_form': u_form, 't_form': t_form})

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

def all_listings(request):
    search_query = request.GET.get('search')
    listings = Listing.objects.all()

    # Filtering logic based on user input
    if search_query:
        listings = listings.filter(Q(title__icontains=search_query) |
            Q(positions__icontains=search_query) |
            Q(location__icontains=search_query))
        
    # Implement this based on your specific filtering requirements

    paginator = Paginator(listings, 10)  # 10 listings per page
    page_number = request.GET.get('page')
    try:
        listings_page = paginator.page(page_number)
    except PageNotAnInteger:
        listings_page = paginator.page(1)
    except EmptyPage:
        listings_page = paginator.page(paginator.num_pages)

    return render(request, 'ffinderapp/all_listings.html', {'listings': listings_page})

def my_listings(request):
    user = request.user
    listings = user.listing_set.all()
    return render(request, 'ffinderapp/my_listings.html', {'listings': listings})

def edit_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == 'POST':
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('listing_detail', listing_id=listing_id)
    else:
        form = ListingForm(instance=listing)
    return render(request, 'ffinderapp/edit_listing.html', {'form': form})

def delete_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.method == 'POST':
        listing.delete()
        return redirect('profile')  # Redirect to profile page after deleting
    return render(request, 'confirm_delete_listing.html', {'listing': listing})


"""
def contact_poster(request):
    if request.method == 'POST':
        message_content = request.POST.get('message')
        sender_email = request.POST.get('contactEmail')
        listing_id = request.POST.get('listing_id')  # Assuming you have a hidden input field for listing ID in your form

        # Save message to database
        message = Message.objects.create(
            content=message_content,
            sender_email=sender_email,
            listing_id=listing_id
        )

        # Send email notification to poster
        send_mail(
            'New message from Football Finder',
            f'You have received a new message from {sender_email}:\n\n{message_content}',
            settings.EMAIL_HOST_USER,  # Sender's email
            ['colley23m@gmail.com'],  # Poster's email (change to actual email address)
            fail_silently=False,
        )

        return redirect('home')  # Redirect to homepage after sending message

    return render(request, 'ffinderapp/contact_poster.html')
"""

class ChatView(View):
    def get(self, request):
        return render(request, 'chat.html')

    def post(self, request):
        # Handle form submission or any other POST requests
        pass

class ChatConsumerView(View):
    def post(self, request):
        # Handle HTTP POST requests for WebSocket messages
        pass

    def websocket_connect(self, message):
        # Accept the WebSocket connection
        message.reply_channel.send({'accept': True})

    def websocket_receive(self, message):
        # Handle incoming WebSocket messages
        text = message.content['text']
        data = json.loads(text)

        # Broadcast the received message to all WebSocket clients
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'chat_group',
            {
                'type': 'chat_message',
                'message': data['message']
            }
        )

    def chat_message(self, event):
        # Send the received message to WebSocket clients
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))