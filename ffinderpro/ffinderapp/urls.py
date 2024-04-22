from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import (
    home,
    player_signup,
    signup,
    login_view,
    profile,
    team_signup,
    player_profile,
    team_profile
)

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('profile/', profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('player_signup/', player_signup, name='player_signup'),
    path('team_signup/', team_signup, name='team_signup'),
    path('create_listing/', views.create_listing, name='create_listing'),
    path('listing/<int:listing_id>/', views.listing_detail, name='listing_detail'),
    path('all-listings/', views.all_listings, name='all_listings'),
    path('my-listings', views.my_listings, name='my_listings'),
    path('player-profile/', player_profile, name='player_profile'),
    path('team-profile/', team_profile, name='team_profile'),
    # Adjust the URL pattern for the profile view to redirect based on user selection
    path('profile/', views.redirect_to_profile, name='redirect_to_profile'),
    #path('profile/<str:username>/', views.profile, name='profile'),
    path('edit-listing/<int:listing_id>/', views.edit_listing, name='edit_listing'),
    path('delete-listing/<int:listing_id>/', views.delete_listing, name='delete_listing'),
    path('path/to/endpoint', views.ajax_view, name='ajax_endpoint'),
    path('send-message/', views.send_message, name='send_message'),
    path('get-messages/', views.get_messages, name='get_messages'),
    path('player_listing/<int:pk>/', views.player_listing_detail, name='player_listing_detail'),
    path('create_player_listing/', views.create_player_listing, name='create_player_listing'),
    path('find_players/', views.find_players, name='find_players'),
    path('post_ad/', views.post_ad, name='post_ad'),
]
