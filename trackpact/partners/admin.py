from django.contrib import admin
from .models import PartnerRequest

@admin.register(PartnerRequest)
class PartnerRequestAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver_email', 'receiver', 'status', 'created_at']
    list_filter = ['status']
