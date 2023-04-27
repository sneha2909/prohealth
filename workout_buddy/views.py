from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseNotAllowed
from django.contrib import messages
from django.views import View
from .forms import SignUpForm, ProfileForm, UserForm, WorkoutForm
from.models import Workout
from webapp.models import User
from webapp.views import loginregister, login_required
from fuzzywuzzy import fuzz
from django.core.mail import send_mail


@login_required
def index(request):
    user_activity = request.user.profile.activity1
    context = {
        'user_activity': user_activity,
    }
    return render(request, 'workout_buddy/landing.html',context)

@login_required
def about(request):
    return render(request, 'workout_buddy/about.html')


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
    return render(request, 'workout_buddy/friends.html', context)


@login_required
def profile(request):
    user = request.user
    workouts = Workout.objects.all().order_by('-time')
    context = {
        'user': user,
        'workouts': workouts,
    }
    return render(request, 'workout_buddy/profile.html', context)


@login_required
def profile_edit(request):
    if request.method == 'POST':
        user = User.objects.get(id = request.user.id)
        user.username = request.POST.get('username','')
        user.name = request.POST.get('name','')
        user.gender=request.POST.get('gender','')
        user.dob=request.POST.get('dob','')
        user.pincode=request.POST.get('pincode','')
        user.location=request.POST.get('location','')
        user.fav_gym_act1=request.POST.get('fav1','')
        user.fav_gym_act2=request.POST.get('fav2','')
        user.save()
        messages.success(request, f'Your changes have been updated')
        return redirect('profile')
        # user.age=request.POST.get('age','')
		# user.height=request.POST.get('height','')
		# user.curr_wght=request.POST.get('curr_wt','')
		# user.tar_wght=request.POST.get('tar_wt','')
		# user.bmi=request.POST.get('bmi','')
    return render(request, 'workout_buddy/profile_edit.html', locals())
	# 	return redirect('school-feed', request.user.student.school.user.slug)
    # return redirect(request, 'home',request.user.slug)

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
    return render(request, 'workout_buddy/workout.html', {
        'form': form,
    })

def message(request):
    send_mail(
        'Connection Request', #subject
        'Let us connect and start working out together!', #message
        request.user.email,
        ['pushtikothi6@gmail.com'],
        fail_silently=False,
    )
