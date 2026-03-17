from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/',          views.dashboard,     name='dashboard'),
    path('workouts/add/',       views.add_workout,   name='add_workout'),
    path('workouts/',           views.workout_list,  name='workout_list'),
    path('workouts/<int:workout_id>/delete/', views.delete_workout, name='delete_workout'),
]
