"""
partners/models.py
-------------------
The PartnerRequest model tracks who invited whom and whether
the invite was accepted.

Flow:
  1. User A sends invite to someone@email.com
  2. That person registers/logs in
  3. They see a pending request and accept it
  4. Both users are linked as partners (via UserProfile.partner)
"""

from django.db import models
from django.contrib.auth.models import User


class PartnerRequest(models.Model):
    """
    Represents a partnership invite from one user to another (by email).
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),    # Invite sent, not yet accepted
        ('accepted', 'Accepted'),  # Both users are now partners
        ('declined', 'Declined'),  # Receiver said no
    ]

    # The user who sent the invite
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_requests'
    )

    # The email the invite was sent to (the receiver might not have an account yet)
    receiver_email = models.EmailField()

    # Once the receiver registers/logs in, we link to their actual User object
    receiver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='received_requests'
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} → {self.receiver_email} ({self.status})"
