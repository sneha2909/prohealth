from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout
# from .models import User
from django.contrib import messages
# Create your views here.
def home(request):
	return render(request,'webapp/home.html')


def loginregister(request):
    logout(request)
    # if request.method == 'POST':
    #     form = request.POST.get('type')
    #     print(form)
    #     if form=='register':
    #         username = request.POST.get('username')
    #         name = request.POST.get('name')
    #         passw = request.POST.get('password')
    #         cpassw = request.POST.get('con_password')
    #         if passw != cpassw:
    #             return render(request, 'webapp/loginregister.html', {'message': 'Password Doesnt Match'})
    #         if User.objects.filter(username=username).exists():
    #             return render(request, 'webapp/loginregister.html', {'message': 'Username Already exists'})
    #         user = User.objects.create(username=username, name=name)
    #         print(user)
    #         user.set_password(passw)
    #         user.save()
    #         user = authenticate(request, username=username, password = passw)
    #         login(request,user)
    #         return redirect('user-details')
    #     elif form=='sign-in':
    #         username = request.POST.get('username')
    #         passw = request.POST.get('password')
    #         user = authenticate(request, username=username, password=passw)
    #         if user is not None:
    #             return redirect('user_forum')
    #         else:
    #             return render(request, 'webapp/loginregister.html', {'message': 'Username or password is incorrect'})
    return render(request, 'webapp/loginregister.html')


def user_details(request):
	print('HEHU')
	# if request.method == 'POST':
	# 	user = User.objects.get(id = request.user.id)
	# 	user.phone_number = request.POST.get('pno','')
	# 	user.email = request.POST.get('email','')
	# 	user.gender=request.POST.get('gender','')
	# 	user.age=request.POST.get('age','')
	# 	user.height=request.POST.get('height','')
	# 	user.curr_wght=request.POST.get('curr_wt','')
	# 	user.tar_wght=request.POST.get('tar_wt','')
	# 	user.bmi=request.POST.get('bmi','')
	# 	user.save()  
	# 	messages.success(request, f'Your account has been created! You are now able to log in')
	# 	return redirect('school-feed', request.user.student.school.user.slug)
	return render(request, 'webapp/user_details.html')

def logout_view(request):
	logout(request)
	return redirect('home')



