from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseNotAllowed
from django.contrib.auth import logout, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
# from .backend import authenticate
from .forms import SignUpForm, ProfileForm, UserForm, WorkoutForm
from.models import Workout
from django.contrib.auth.models import User
from fuzzywuzzy import fuzz
@login_required
def friends(request):
    friend_list = []
    friend_list_2 = []
    current_user = request.user
    users = User.objects.all()
    for user in users:
        if fuzz.ratio(current_user.profile.activity1, user.profile.activity1) > 85 and user != current_user:
            friend_list.append(user)
    for user in users:
        if fuzz.ratio(current_user.profile.activity2, user.profile.activity2) > 85 and user != current_user:
            friend_list_2.append(user)
    context = {
        'friend_list': friend_list,
        'friend_list_2': friend_list_2,
        'current_user': current_user,
    }
    return render(request, 'main/friends.html', context)


@login_required
def profile(request):
    user = request.user
    workouts = Workout.objects.all().order_by('-time')
    context = {
        'user': user,
        'workouts': workouts,
    }
    return render(request, 'main/profile.html', context)


@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            print('Profile successfully updated.')
            return redirect('/profile')
        else:
            print('Error!')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'main/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
def workout(request):
    if request.method == "POST":
        form = WorkoutForm(request.POST)
        if form.is_valid():
            form.save()
            print('Workout successfully logged.')
            return redirect('/profile')
        else:
            print("Error!")
    else:
        form = WorkoutForm()
    return render(request, 'main/workout.html', {
        'form': form,
    })

