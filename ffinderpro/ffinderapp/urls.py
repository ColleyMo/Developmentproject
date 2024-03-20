from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home, player_signup, signup, login_view, profile, team_signup


urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('profile/', profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('player_signup/', player_signup, name='player_signup'),
    path('team_signup/', team_signup, name='team_signup'),
    

]
