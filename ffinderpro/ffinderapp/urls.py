from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home, signup, login_view, profile


urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('profile/', profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')

]
