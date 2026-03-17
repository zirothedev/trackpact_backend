from django.contrib import admin
from .models import Workout

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'duration', 'date']
    list_filter = ['date', 'user']
    search_fields = ['title', 'user__username']
