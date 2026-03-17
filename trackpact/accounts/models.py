"""
accounts/models.py
------------------
We extend Django's built-in User model with a simple UserProfile.
This keeps things simple — we don't replace the User model,
we just attach extra info to it via a OneToOneField.
"""

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Extra info for each user.
    Created automatically when a user registers (see accounts/views.py).
    """

    # Each user has exactly one profile
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Optional fitness goal (e.g. "Run 5k by June")
    fitness_goal = models.TextField(blank=True, null=True)

    # The user's accountability partner (another User)
    # null=True means they might not have a partner yet
    partner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='partner_of',  # lets us do partner_user.partner_of.all()
    )

    def __str__(self):
        return f"{self.user.username}'s profile"
