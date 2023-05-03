from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib import messages
from .models import User_Info, User_Exercise_Info, Playlist_Check, Diet_Menu
import pandas as pd
# Create your views here.


def home(request):
    return render(request, 'webapp/home.html')


def loginregister(request):
    logout(request)
    if request.method == 'POST':
        form = request.POST.get('type')
        print(form)
        if form == 'register':
            username = request.POST.get('username')
            name = request.POST.get('name')
            passw = request.POST.get('password')
            cpassw = request.POST.get('con_password')
            if passw != cpassw:
                return render(request, 'webapp/loginregister.html', {'message': 'Password Doesnt Match'})
            if User.objects.filter(username=username).exists():
                return render(request, 'webapp/loginregister.html', {'message': 'Username Already exists'})
            user = User.objects.create(username=username, name=name)
            print(user)
            user.set_password(passw)
            user.save()
            user = authenticate(request, username=username, password=passw)
            login(request, user)
            return redirect('user-details')
        elif form == 'sign-in':
            username = request.POST.get('username')
            passw = request.POST.get('password')
            user = authenticate(request, username=username, password=passw)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'webapp/loginregister.html', {'message': 'Username or password is incorrect'})
    return render(request, 'webapp/loginregister.html')


def user_details(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        user.phone_number = request.POST.get('pno', '')
        user.email = request.POST.get('email', '')
        user.gender = request.POST.get('gender', '')
        user.dob = request.POST.get('dob', '')
        user.age=request.POST.get('age', '')
        user.height=request.POST.get('height', '')
        user.weight=request.POST.get('weight', '')
        user.activity_level=request.POST.get('act_lvl', '')
        user.pincode = request.POST.get('pincode', '')
        user.location = request.POST.get('location', '')
        user.fav_gym_act1 = request.POST.get('fav1', '')
        user.fav_gym_act2 = request.POST.get('fav2', '')
        user.save()
        messages.success(
            request, f'Your account has been created! You are now able to log in')
        return render(request, 'webapp/home.html')
        # user.age=request.POST.get('age','')
        # user.height=request.POST.get('height','')
        # user.curr_wght=request.POST.get('curr_wt','')
        # user.tar_wght=request.POST.get('tar_wt','')
        # user.bmi=request.POST.get('bmi','')
    return render(request, 'webapp/user_details.html', locals())
    # 	return redirect('school-feed', request.user.student.school.user.slug)
    # return redirect(request, 'home',request.user.slug)


def home(request):
    if request.user.is_authenticated:
        print("User is logged in :)")
        print(f"Username --> {request.user.username}")
    else:
        print("User is not logged in :(")
    return render(request, 'webapp/home.html', {'user': request.user})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):

    return render(request, 'webapp/workout_dashboard.html')


def progress(request):

    # user_data = User.objects.filter(
    #     user_email=request.session['user_mail_id']).first()
    # user_data_exercise = User_Exercise_Info.objects.filter(
    #     user_name=user_data.user_name)
    # playlist_status = Playlist_Check.objects.filter(
    #     user_email=request.session['user_mail_id'])

    # df = pd.DataFrame(None)
    # df = pd.DataFrame(user_data_exercise.values())
    # df["current_time"] = pd.to_datetime(df["current_time"]).dt.date
    # df = df.groupby(['current_time']).sum()

    # x_axis = df.index.tolist()
    # y_axis = df['exercise_calorie_burnt'].tolist()

    # y1_axis = df['exercise_weight_loss'].multiply(10000).tolist()

    # exercise_duration = df['exercise_duration'].sum().tolist()

    # calories_burnt = df['exercise_calorie_burnt'].sum().tolist()

    # playlist_lt = [list(i.values()) for i in playlist_status.values()]
# return render parameter
# {'user_data': user_data,
#                                              'user_data_exercise': user_data_exercise,
#                                              'x_axis': x_axis,
#                                              'y_axis': y_axis,
#                                              'y1_axis': y1_axis,
#                                              'exercise_duration': round(exercise_duration/60, 2),
#                                              'calories_burnt': round(calories_burnt, 2),
#                                              'playlist_lt': playlist_lt[0][2:9]}
    return render(request, 'webapp/progress.html', )

def diet_recommend(request):
    return render(request, 'webapp/diet-recommendation.html')