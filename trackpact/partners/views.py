"""
partners/views.py
------------------
Handles partner page, invites, accepting/declining, reminders, and removal.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from .models import PartnerRequest
from .forms import PartnerInviteForm, ReminderForm
from accounts.models import UserProfile
from workouts.models import Workout


@login_required
def partner_page(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    # Requests this user sent
    sent_requests = PartnerRequest.objects.filter(sender=request.user).order_by('-created_at')

    # Requests this user received (match by email)
    received_requests = PartnerRequest.objects.filter(
        receiver_email=request.user.email,
        status='pending'
    )
    # Link receiver field if not set yet
    for req in received_requests:
        if req.receiver is None:
            req.receiver = request.user
            req.save()

    # Partner stats (streak, total, this week)
    partner_streak = 0
    partner_total_workouts = 0
    partner_this_week = 0

    if profile.partner:
        today      = timezone.now().date()
        start_week = today - timedelta(days=today.weekday())

        partner_total_workouts = Workout.objects.filter(user=profile.partner).count()
        partner_this_week      = Workout.objects.filter(user=profile.partner, date__gte=start_week, date__lte=today).count()

        # Streak calculation
        check_date = today
        while Workout.objects.filter(user=profile.partner, date=check_date).exists():
            partner_streak += 1
            check_date -= timedelta(days=1)

    return render(request, 'partners/partner_page.html', {
        'profile':               profile,
        'sent_requests':         sent_requests,
        'received_requests':     received_requests,
        'partner_streak':        partner_streak,
        'partner_total_workouts': partner_total_workouts,
        'partner_this_week':     partner_this_week,
    })


@login_required
def send_invite(request):
    if request.method == 'POST':
        form = PartnerInviteForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            if email == request.user.email:
                messages.error(request, "You can't invite yourself!")
                return redirect('partner_page')

            already_sent = PartnerRequest.objects.filter(
                sender=request.user, receiver_email=email, status='pending'
            ).exists()

            if already_sent:
                messages.warning(request, f"You already sent an invite to {email}.")
                return redirect('partner_page')

            invite = PartnerRequest.objects.create(sender=request.user, receiver_email=email)

            try:
                receiver_user = User.objects.get(email=email)
                invite.receiver = receiver_user
                invite.save()
            except User.DoesNotExist:
                pass

            send_mail(
                subject=f"[TrackPact] {request.user.username} wants to be your accountability partner!",
                message=(
                    f"Hi there!\n\n"
                    f"{request.user.username} has invited you to be their workout accountability partner on TrackPact.\n\n"
                    f"Sign up or log in at: http://127.0.0.1:8000/accounts/register/\n"
                    f"Then go to the Partners page to accept.\n\n"
                    f"— The TrackPact Team"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=True,
            )

            messages.success(request, f"Invite sent to {email}! 📧")
            return redirect('partner_page')
    else:
        form = PartnerInviteForm()

    # Pass sent_requests so the page can show the list
    sent_requests = PartnerRequest.objects.filter(sender=request.user).order_by('-created_at')

    return render(request, 'partners/send_invite.html', {
        'form': form,
        'sent_requests': sent_requests,
    })


@login_required
def accept_request(request, request_id):
    invite = get_object_or_404(
        PartnerRequest, id=request_id,
        receiver_email=request.user.email, status='pending'
    )
    invite.receiver = request.user
    invite.status   = 'accepted'
    invite.save()

    sender_profile, _ = UserProfile.objects.get_or_create(user=invite.sender)
    sender_profile.partner = request.user
    sender_profile.save()

    receiver_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    receiver_profile.partner = invite.sender
    receiver_profile.save()

    messages.success(request, f"You and {invite.sender.username} are now accountability partners! 🤝")
    return redirect('partner_page')


@login_required
def decline_request(request, request_id):
    invite = get_object_or_404(
        PartnerRequest, id=request_id,
        receiver_email=request.user.email, status='pending'
    )
    invite.status = 'declined'
    invite.save()
    messages.info(request, "Invite declined.")
    return redirect('partner_page')


@login_required
def send_reminder(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if not profile.partner:
        messages.error(request, "You don't have a partner yet. Invite someone first!")
        return redirect('partner_page')

    partner = profile.partner

    if not partner.email:
        messages.error(request, "Your partner doesn't have an email on file.")
        return redirect('partner_page')

    if request.method == 'POST':
        form = ReminderForm(request.POST)
        if form.is_valid():
            custom_message = form.cleaned_data['message']

            send_mail(
                subject=f"[TrackPact] 💪 Reminder from {request.user.username}!",
                message=(
                    f"Hi {partner.first_name or partner.username},\n\n"
                    f"Your accountability partner {request.user.username} sent you a reminder:\n\n"
                    f'"{custom_message}"\n\n'
                    f"Log your workout: http://127.0.0.1:8000/workouts/add/\n\n"
                    f"— The TrackPact Team"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[partner.email],
                fail_silently=False,
            )

            messages.success(request, f"Reminder sent to {partner.username}! 🚀")
            return redirect('partner_page')
    else:
        form = ReminderForm()

    return render(request, 'partners/send_reminder.html', {
        'form': form,
        'partner': partner,
    })


@login_required
def remove_partner(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if profile.partner:
        try:
            partner_profile = UserProfile.objects.get(user=profile.partner)
            if partner_profile.partner == request.user:
                partner_profile.partner = None
                partner_profile.save()
        except UserProfile.DoesNotExist:
            pass

        profile.partner = None
        profile.save()
        messages.info(request, "Partner removed.")

    return redirect('partner_page')
