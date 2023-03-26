from calorie_tracker_app.apps import CalorieTrackerAppConfig
from django.urls import path
from . import views

# app_name = "calorie_tracker_app"

urlpatterns = [
    path('', views.calorie_tracker, name="index"),
    path('delete/<int:id>', views.delete_consume, name="delete_consume"),
]