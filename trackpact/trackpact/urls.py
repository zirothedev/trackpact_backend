"""
TrackPact URL Configuration
----------------------------
This is the main URL file. It connects all app URLs together.
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required


def landing(request):
    """
    FIX: Previously this was a raw TemplateView which had no way to check
    if the user was already logged in. A logged-in user visiting '/' would
    just see the landing page with login/register buttons again.

    Now we check request.user.is_authenticated first:
    - Logged-in user  → redirect straight to dashboard
    - Logged-out user → show the landing page normally
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'base/landing.html')


urlpatterns = [
    # Django admin panel
    path('admin/', admin.site.urls),

    # Landing page at "/" — now uses a smart view instead of TemplateView
    path('', landing, name='landing'),

    # accounts app handles: register, login, logout, profile
    path('accounts/', include('accounts.urls')),

    # workouts app handles: dashboard, add workout, list workouts
    path('', include('workouts.urls')),

    # partners app handles: send invite, accept invite, send reminder
    path('partners/', include('partners.urls')),
]
