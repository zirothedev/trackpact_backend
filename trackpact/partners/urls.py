"""
partners/urls.py
-----------------
URL patterns for the partners app.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Main partners page — see status, sent/received invites
    path('', views.partner_page, name='partner_page'),

    # Send an invite to a new partner
    path('invite/', views.send_invite, name='send_invite'),

    # Accept an invite (request_id from URL)
    path('accept/<int:request_id>/', views.accept_request, name='accept_request'),

    # Decline an invite
    path('decline/<int:request_id>/', views.decline_request, name='decline_request'),

    # Send a reminder to your partner
    path('remind/', views.send_reminder, name='send_reminder'),

    # Remove your current partner
    path('remove/', views.remove_partner, name='remove_partner'),
]
