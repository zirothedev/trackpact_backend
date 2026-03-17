"""
accounts/urls.py
-----------------
URL patterns for the accounts app.
We use Django's built-in auth views for login and logout.
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Our custom register view
    path('register/', views.register, name='register'),

    # FIX: Added redirect_authenticated_user=True so that if a logged-in
    # user visits /accounts/login/ they get sent to dashboard instead of
    # seeing the login form (which makes it look like they're logged out).
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        redirect_authenticated_user=True,  # <-- this is the key fix
    ), name='login'),

    # Django's built-in logout view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Our profile view
    path('profile/', views.profile, name='profile'),
]
