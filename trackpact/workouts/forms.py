"""
workouts/forms.py
------------------
Form for logging a new workout.
"""

from django import forms
from .models import Workout


class WorkoutForm(forms.ModelForm):
    class Meta:
        model  = Workout
        fields = ['title', 'category', 'duration', 'date', 'notes']
        widgets = {
            'date':     forms.DateInput(attrs={'type': 'date'}),
            'notes':    forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any notes? (optional)'}),
            'title':    forms.TextInput(attrs={'placeholder': 'e.g. Morning Run, Chest Day'}),
            'duration': forms.NumberInput(attrs={'placeholder': 'Minutes'}),
        }
