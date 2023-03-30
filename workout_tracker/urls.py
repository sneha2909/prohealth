from django.urls import re_path as url
from django.urls import path
from . import views

urlpatterns = [
    # url(r'^$', views.login), # index / login page
    # url(r'^user/register$', views.register), # get register page / register user
    # url(r'^user/login$', views.login), # logs in existing user
    # url(r'^user/logout$', views.logout), # destroys user session
<<<<<<< HEAD
    # url(r'^$', views.dashboard),
    path('', views.dashboard, name='workout-tracker'),# get dashboard
    url(r'^workout$', views.new_workout),# get workout page / add workout
    url(r'^workout/(?P<id>\d*)$', views.workout), # get workout / update workout
    url(r'^workout/(?P<id>\d*)/exercise$', views.exercise), # add exercise
    url(r'^workout/(?P<id>\d*)/complete$', views.complete_workout), # complete workout
    url(r'^workout/(?P<id>\d*)/edit$', views.edit_workout), # edit workout
    url(r'^workout/(?P<id>\d*)/delete$', views.delete_workout), # delete workout
    url(r'^workouts$', views.all_workouts), # get all workouts
    url(r'^legal/tos$', views.tos), # get terms of service
=======
    url(r'^dashboard$', views.dashboard,name='workout-tracker'), # get dashboard
    url(r'^workout$', views.new_workout,name='new-workout'), # get workout page / add workout
    url(r'^workout/(?P<id>\d*)$', views.workout, name='get-workout'), # get workout / update workout
    url(r'^workout/(?P<id>\d*)/exercise$', views.exercise,name='add-exercise'), # add exercise
    url(r'^workout/(?P<id>\d*)/complete$', views.complete_workout,name='complete-workout'), # complete workout
    url(r'^workout/(?P<id>\d*)/edit$', views.edit_workout,name='edit-workout'), # edit workout
    url(r'^workout/(?P<id>\d*)/delete$', views.delete_workout,name='delete-workout'), # delete workout
    url(r'^workouts$', views.all_workouts,name='all-workout'), # get all workouts
    url(r'^legal/tos$', views.tos,name='tos'), # get terms of service
>>>>>>> a4275b44620b34b35e5612c6204b0fc5b5c6c586
]