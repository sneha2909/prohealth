from django.urls import path
from . import views

urlpatterns = [
    # path('$', views.login), # index / login page
    # path('user/register$', views.register), # get register page / register user
    # path('user/login$', views.login), # logs in existing user
    # path('user/logout$', views.logout), # destroys user session
    path('', views.dashboard,name='workout-tracker'), # get dashboard
    path('workout/', views.new_workout,name='new-workout'), # get workout page / add workout
    path('workout(?P<id>\d*)/', views.workout,name='get-workout'), # get workout / update workout
    path('workout/exercise/(?P<id>\d*)/', views.exercise,name='add-exercise'),  # add exercise
    path('workout/complete(?P<id>\d*)/', views.complete_workout,name='complete-workout'), # complete workout
    path('workout/edit(?P<id>\d*)/', views.edit_workout,name='edit-workout'), # edit workout
    path('workout/delete(?P<id>\d*)/', views.delete_workout,name='delete-workout'), # delete workout
    path('workouts/', views.all_workouts,name='all-workout'), # get all workouts
    path('legal/tos/', views.tos,name='tos'), # get terms of service
]