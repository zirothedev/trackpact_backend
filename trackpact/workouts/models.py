"""
workouts/models.py
-------------------
The Workout model stores each workout a user logs.
Added a 'category' field for workout type selection.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Workout(models.Model):

    CATEGORY_CHOICES = [
        ('strength',    'Strength'),
        ('cardio',      'Cardio'),
        ('flexibility', 'Flexibility'),
        ('sports',      'Sports'),
        ('other',       'Other'),
    ]

    user     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
    title    = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    date     = models.DateField(default=timezone.now)
    notes    = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title} on {self.date}"
