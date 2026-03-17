from django.contrib import admin
from .models import UserProfile

# Register UserProfile so we can see/edit it in the admin panel
admin.site.register(UserProfile)
