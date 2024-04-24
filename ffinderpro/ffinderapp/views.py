from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SignUpForm, PlayerSignUpForm, TeamSignUpForm, ListingForm, ProfileUpdateForm, PlayerProfileForm, TeamProfileForm, PlayerListingForm
from .models import CustomUser, PlayerProfile, TeamProfile, Listing, PlayerListing
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from .models import Message
from django.http import HttpResponse, JsonResponse
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
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            registration_type = form.cleaned_data['registration_type']

            # Create a CustomUser instance
            user = CustomUser.objects.create_user(username=username, password=password)

            if registration_type == 'player':
                # Create a PlayerProfile instance and associate with user
                PlayerProfile.objects.create(user=user)
                return redirect('player_profile')
            elif registration_type == 'team':
                # Create a TeamProfile instance and associate with user
                TeamProfile.objects.create(user=user)
                return redirect('team_profile')

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
def redirect_to_profile(request):
    if request.user.is_player:
        return redirect('player_profile')
    elif request.user.is_team:
        return redirect('team_profile')
    else:
        # Handle the case when user is not associated with any profile type
        # You can redirect them to a generic profile page or handle this case as per your requirement
        pass

def profile(request):
    user = request.user
    u_form = ProfileUpdateForm(instance=user)
    p_form = PlayerProfileForm()  # Initialize p_form here
    t_form = TeamProfileForm()

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
    user_profile = listing.user_profile
    return render(request, 'ffinderapp/listing_detail.html', {'listing': listing, 'user_profile': user_profile})

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


def ajax_view(request):
    # Process the AJAX request and return a JSON response
    data = {'message': 'AJAX request received successfully!'}
    return JsonResponse(data)


def send_message(request):
    if request.method == 'POST':
        sender = request.user
        recipient_id = request.POST.get('recipient_id')
        content = request.POST.get('content')
        if recipient_id and content:
            recipient = CustomUser.objects.get(id=recipient_id)
            message = Message.objects.create(sender=sender, recipient=recipient, content=content)
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def get_messages(request):
    if request.method == 'GET':
        sender_id = request.GET.get('sender_id')
        recipient_id = request.GET.get('recipient_id')
        if sender_id and recipient_id:
            messages = Message.objects.filter(sender_id=sender_id, recipient_id=recipient_id)
            data = [{'sender': message.sender.username, 'content': message.content, 'timestamp': message.timestamp} for message in messages]
            return JsonResponse({'messages': data})
    return JsonResponse({'messages': []})

def create_player_listing(request):
    if request.method == 'POST':
        form = PlayerListingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('find_players')
    else:
        form = PlayerListingForm()
    return render(request, 'ffinderapp/create_player_listing.html', {'form': form})

def find_players(request):
    search_query = request.GET.get('search')
    player_listings = PlayerListing.objects.all()

    # Filtering logic based on user input
    if search_query:
        player_listings = player_listings.filter(Q(title__icontains=search_query) |
                                                 Q(position__icontains=search_query))
        
    # Pagination
    paginator = Paginator(player_listings, 10)  # 10 player listings per page
    page_number = request.GET.get('page')
    try:
        player_listings_page = paginator.page(page_number)
    except PageNotAnInteger:
        player_listings_page = paginator.page(1)
    except EmptyPage:
        player_listings_page = paginator.page(paginator.num_pages)

    return render(request, 'ffinderapp/find_players.html', {'player_listings': player_listings_page})

def post_ad(request):
    return render(request, 'ffinderapp/post_ad.html')

def player_listing_detail(request, pk):
    # Retrieve the player listing object based on the provided primary key (pk)
    try:
        player_listing = PlayerListing.objects.get(pk=pk)
    except PlayerListing.DoesNotExist:
        return HttpResponse("Player listing not found.", status=404)
    
    # Render the template with the player listing object
    return render(request, 'ffinderapp/player_listing_detail.html', {'player_listing': player_listing})