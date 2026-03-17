"""
accounts/views.py
------------------
Handles: Register, Login, Logout, Profile.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum

from .forms import RegisterForm, ProfileForm, UserInfoForm
from .models import UserProfile
from workouts.models import Workout


def register(request):
    """
    FIX: Added a check at the top — if the user is already logged in
    and somehow lands on /register/, redirect them to dashboard instead
    of showing the register form again (which would look like they're
    logged out).
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user       = form.save()
            user.email = form.cleaned_data['email']
            user.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, f"Welcome to TrackPact, {user.username}! 🎉")
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    today      = timezone.now().date()
    start_week = today - timedelta(days=today.weekday())

    # Workout stats
    total_workouts = Workout.objects.filter(user=request.user).count()
    total_minutes  = Workout.objects.filter(user=request.user).aggregate(
        total=Sum('duration')
    )['total'] or 0
    this_week = Workout.objects.filter(
        user=request.user, date__gte=start_week, date__lte=today
    ).count()

    # Current streak
    streak     = 0
    check_date = today
    while Workout.objects.filter(user=request.user, date=check_date).exists():
        streak    += 1
        check_date -= timedelta(days=1)

    # Handle all 3 forms — each has its own submit button with a hidden 'action' field
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_info':
            user_info_form = UserInfoForm(request.POST, instance=request.user)
            profile_form   = ProfileForm(instance=user_profile)
            password_form  = PasswordChangeForm(request.user)
            if user_info_form.is_valid():
                user_info_form.save()
                messages.success(request, "Personal info updated!")
                return redirect('profile')

        elif action == 'update_goal':
            profile_form   = ProfileForm(request.POST, instance=user_profile)
            user_info_form = UserInfoForm(instance=request.user)
            password_form  = PasswordChangeForm(request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Fitness goal updated!")
                return redirect('profile')

        elif action == 'change_password':
            password_form  = PasswordChangeForm(request.user, request.POST)
            user_info_form = UserInfoForm(instance=request.user)
            profile_form   = ProfileForm(instance=user_profile)
            if password_form.is_valid():
                user = password_form.save()
                # Keep user logged in after password change
                update_session_auth_hash(request, user)
                messages.success(request, "Password changed successfully!")
                return redirect('profile')
        else:
            user_info_form = UserInfoForm(instance=request.user)
            profile_form   = ProfileForm(instance=user_profile)
            password_form  = PasswordChangeForm(request.user)

    else:
        user_info_form = UserInfoForm(instance=request.user)
        profile_form   = ProfileForm(instance=user_profile)
        password_form  = PasswordChangeForm(request.user)

    return render(request, 'accounts/profile.html', {
        'user_info_form': user_info_form,
        'profile_form':   profile_form,
        'password_form':  password_form,
        'user_profile':   user_profile,
        'total_workouts': total_workouts,
        'total_minutes':  total_minutes,
        'this_week':      this_week,
        'streak':         streak,
    })
