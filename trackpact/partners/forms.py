"""
partners/forms.py
------------------
Forms for sending a partner invite and sending a reminder.
"""

from django import forms


class PartnerInviteForm(forms.Form):
    """
    Simple form: just enter the email of the person you want as partner.
    """
    email = forms.EmailField(
        label="Partner's Email",
        widget=forms.EmailInput(attrs={'placeholder': "partner@example.com"})
    )


class ReminderForm(forms.Form):
    """
    Simple form: write a short message to send to your partner.
    """
    message = forms.CharField(
        label="Your message",
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': "Hey! Don't forget to log your workout today! 💪"
        }),
        max_length=500,
    )
