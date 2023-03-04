"""prohealth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# from django.conf.urls import url
# from . import views
# from calorie_tracker_app.apps import CalorieTrackerAppConfig
from django.urls import path
from webapp.views import home

# app_name = CalorieTrackerAppConfig.name

urlpatterns = [
    path('admin/', admin.site.urls),
    # path(r'^$', views.login), # index / login page
    # path(r'^user/register$', views.register), # get register page / register user
    # path(r'^user/login$', views.login), # logs in existing user
    # path(r'^user/logout$', views.logout), # destroys user session
    # path(r'^dashboard$', views.dashboard), # get dashboard
    # path(r'^workout$', views.new_workout), # get workout page / add workout
    # path(r'^workout/(?P<id>\d*)$', views.workout), # get workout / update workout
    # path(r'^workout/(?P<id>\d*)/exercise$', views.exercise), # add exercise
    # path(r'^workout/(?P<id>\d*)/complete$', views.complete_workout), # complete workout
    # path(r'^workout/(?P<id>\d*)/edit$', views.edit_workout), # edit workout
    # path(r'^workout/(?P<id>\d*)/delete$', views.delete_workout), # delete workout
    # path(r'^workouts$', views.all_workouts), # get all workouts
    # path(r'^legal/tos$', views.tos), # get terms of service
    # # path("", views.forum, name="forum"),
    # path("add_post", views.add_post, name="forum_add_post"),
    # path("post/<str:slug>", views.post_detail, name="forum_post_detail"),
    # path("add_comment", views.add_comment, name="forum_add_comment"),
    # path("delete_post", views.delete_post, name="forum_delete_post"),
    # path("delete_comment", views.delete_comment, name="forum_delete_comment"),
    # path("counselor-forum", views.counselor_forum, name="counselor_forum"),
    path('', home, name='home'),
    # path('delete/<int:id>', delete_consume, name="delete_consume"),
    # path('', views.index, name='index'),
    # path('about/', views.about, name='about'),
    # path('workout/', views.workout, name='workout'),
    # path('friends/', views.friends, name='friends'),
    # path('profile/', views.profile, name='profile'),
    # path('profile_edit/', views.profile_edit, name='profile_edit'),
]



   