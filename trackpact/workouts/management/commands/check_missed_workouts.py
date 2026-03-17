"""
workouts/management/commands/check_missed_workouts.py
------------------------------------------------------
This is a Django management command.

Run it manually with:
    python manage.py check_missed_workouts

Or schedule it to run daily at midnight using a cron job:
    0 23 * * * /path/to/venv/bin/python /path/to/manage.py check_missed_workouts

What it does:
    1. Gets all users who have a partner assigned
    2. Checks if each user logged a workout TODAY
    3. If they did NOT → sends an email to their partner
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings

from workouts.models import Workout
from accounts.models import UserProfile


class Command(BaseCommand):
    # This text appears when you run: python manage.py help check_missed_workouts
    help = 'Check for users who missed their workout today and notify their partners.'

    def handle(self, *args, **options):
        today = timezone.now().date()
        self.stdout.write(f"Running missed workout check for {today}...")

        notified_count = 0

        # Loop through every user who has a profile with a partner
        profiles_with_partners = UserProfile.objects.filter(
            partner__isnull=False  # Only users who HAVE a partner
        ).select_related('user', 'partner')

        for profile in profiles_with_partners:
            user = profile.user
            partner = profile.partner

            # Skip if the partner has no email (can't notify them)
            if not partner.email:
                self.stdout.write(f"  Skipping {user.username} — partner has no email.")
                continue

            # Check if the user logged any workout today
            worked_out_today = Workout.objects.filter(user=user, date=today).exists()

            if worked_out_today:
                # Great! They worked out. Nothing to do.
                self.stdout.write(f"  ✓ {user.username} worked out today. No notification needed.")
            else:
                # They missed their workout! Notify the partner.
                self.stdout.write(f"  ✗ {user.username} missed workout. Notifying partner {partner.username}...")

                send_mail(
                    subject=f"[TrackPact] {user.first_name or user.username} missed their workout today!",
                    message=(
                        f"Hi {partner.first_name or partner.username},\n\n"
                        f"Your accountability partner {user.first_name or user.username} "
                        f"hasn't logged a workout today ({today}).\n\n"
                        f"Why not send them a quick reminder to keep them on track? "
                        f"Log in to TrackPact and send them some motivation!\n\n"
                        f"— The TrackPact Team"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[partner.email],
                    fail_silently=False,  # Raise errors so we know if something breaks
                )

                notified_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone! {notified_count} partner(s) were notified about missed workouts."
            )
        )
