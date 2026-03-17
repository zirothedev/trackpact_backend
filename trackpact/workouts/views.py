"""
workouts/views.py
------------------
Dashboard, workout list, add workout, delete workout.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Q

from .models import Workout
from .forms import WorkoutForm
from accounts.models import UserProfile


@login_required
def dashboard(request):
    today      = timezone.now().date()
    start_week = today - timedelta(days=today.weekday())

    workouts = Workout.objects.filter(user=request.user).order_by('-date')[:10]

    workout_dates_qs = (
        Workout.objects.filter(user=request.user)
        .values_list('date', flat=True)
        .order_by('date')
    )
    workout_dates = [str(d) for d in workout_dates_qs]

    worked_out_today   = Workout.objects.filter(user=request.user, date=today).exists()
    workouts_this_week = Workout.objects.filter(user=request.user, date__gte=start_week, date__lte=today).count()

    streak     = 0
    check_date = today
    while Workout.objects.filter(user=request.user, date=check_date).exists():
        streak    += 1
        check_date -= timedelta(days=1)

    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    partner_missed_today = False
    if profile.partner:
        yesterday = today - timedelta(days=1)
        partner_missed_today = not Workout.objects.filter(user=profile.partner, date=yesterday).exists()

    return render(request, 'workouts/dashboard.html', {
        'workouts':             workouts,
        'workout_dates':        workout_dates,
        'worked_out_today':     worked_out_today,
        'workouts_this_week':   workouts_this_week,
        'weekly_target':        4,
        'streak':               streak,
        'profile':              profile,
        'partner_missed_today': partner_missed_today,
        'today':                today,
    })


@login_required
def add_workout(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    # Streak for motivational display
    today      = timezone.now().date()
    streak     = 0
    check_date = today
    while Workout.objects.filter(user=request.user, date=check_date).exists():
        streak    += 1
        check_date -= timedelta(days=1)

    # Last workout logged
    last_workout = Workout.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout      = form.save(commit=False)
            workout.user = request.user
            workout.save()
            messages.success(request, f"Great job! '{workout.title}' logged! 💪")
            return redirect('dashboard')
    else:
        form = WorkoutForm(initial={'date': today})

    return render(request, 'workouts/add_workout.html', {
        'form':         form,
        'streak':       streak,
        'last_workout': last_workout,
        'profile':      profile,
    })


@login_required
def workout_list(request):
    today      = timezone.now().date()
    start_week = today - timedelta(days=today.weekday())

    # Search/filter
    query    = request.GET.get('q', '')
    category = request.GET.get('category', '')

    workouts = Workout.objects.filter(user=request.user)

    if query:
        workouts = workouts.filter(
            Q(title__icontains=query) | Q(notes__icontains=query)
        )

    if category:
        workouts = workouts.filter(category=category)

    # Stats
    total_workouts = Workout.objects.filter(user=request.user).count()
    total_minutes  = Workout.objects.filter(user=request.user).aggregate(
        total=Sum('duration')
    )['total'] or 0
    this_week = Workout.objects.filter(
        user=request.user, date__gte=start_week, date__lte=today
    ).count()

    return render(request, 'workouts/workout_list.html', {
        'workouts':       workouts,
        'total_workouts': total_workouts,
        'total_minutes':  total_minutes,
        'this_week':      this_week,
        'query':          query,
        'category':       category,
        'categories':     Workout.CATEGORY_CHOICES,
    })


@login_required
def delete_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)
    if request.method == 'POST':
        title = workout.title
        workout.delete()
        messages.success(request, f"'{title}' deleted.")
    return redirect('workout_list')
