from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib import messages
# Create your views here.
def home(request):
	return render(request,'webapp/home.html')

# def loginregister(request):
# 	logout(request)
# 	if request.method == 'POST':
# 		form = request.POST.get('type')
# 		print(form)
# 		if form=='register':
# 			cat = request.POST.get('category')
# 			print(cat)
# 			username = request.POST.get('username')
# 			name = request.POST.get('name')
# 			passw = request.POST.get('password')
# 			cpassw = request.POST.get('con_password')
# 			if passw != cpassw:
# 				return render(request, 'profiles/loginregister.html', {'message': 'Password Doesnt Match'})
# 			if User.objects.filter(username=username).exists():
# 				return render(request, 'profiles/loginregister.html', {'message': 'Username Already exists'})
# 			if cat == 'student':
# 				user = User.objects.create(username=username, name=name)
# 				print(user)
# 				user.set_password(passw)
# 				user.save()
# 				user = authenticate(request, username=username, password = passw)
# 				login(request,user)
# 				return redirect('student-register')
# 			elif cat == 'school':
# 				user = User.objects.create(username=username, name=name)
# 				user.set_password(passw)
# 				user.save()
# 				user = authenticate(request, username=username, password = passw)
# 				login(request,user)
# 				return redirect('school-register')
# 			elif cat == 'counselor':
# 				user = User.objects.create(username=username, name=name)
# 				user.set_password(passw)
# 				user.save()
# 				user = authenticate(request, username=username, password = passw)
# 				login(request,user)
# 				return redirect('counselor-register')
# 		elif form=='sign-in':
# 			username = request.POST.get('username')
# 			passw = request.POST.get('password')
# 			user = authenticate(request, username=username, password=passw)
# 			if user is not None:
# 				login(request,user)
# 				if user.is_school:
# 					return redirect('school-feed', user.slug)
# 				elif user.is_student:
# 					return redirect('school-feed',user.student.school.user.slug)
# 				else:
# 					return redirect('counselor_forum')
# 			else:
# 				return render(request, 'webapp/loginregister.html', {'message': 'Username or password is incorrect'})

		

# 	return render(request, 'webapp/loginregister.html')

# def student_register(request):
# 	print('HEHU')
# 	if request.method == 'POST':
# 		user = User.objects.get(id = request.user.id)
# 		user.phone_number = request.POST.get('pno','')
# 		user.email = request.POST.get('email','')
# 		user.is_student = True
# 		# student = Student()
# 		student.user = user
# 		student.roll_number = request.POST.get('rollno','')
# 		school = request.POST.get('schoolname','')
# 		print(school)
# 		student.school = School.objects.get(user_id=school)
# 		student.pincode = request.POST.get('pincode','')
# 		user.std = request.POST.get('standard','')
# 		user.division = request.POST.get('division','')
# 		student.save()
# 		user.save()  
# 		messages.success(request, f'Your account has been created! You are now able to log in')
# 		return redirect('school-feed', request.user.student.school.user.slug)
# 	schools = School.objects.all()
# 	return render(request, 'profiles/student_register.html', locals())

# def logout_view(request):
# 	logout(request)
# 	return redirect('home')