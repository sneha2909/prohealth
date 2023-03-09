from django.shortcuts import render

# Create your views here.
# WORKOUT TRACKER ---------------------------------------------------------------------------------------------------------------------
from django.shortcuts import render, redirect
from django.contrib import messages # access django's `messages` module.
from .models import User, Workout, Exercise
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def login(request):
    """If GET, load login page, if POST, login user."""

    if request.method == "GET":
        return render(request, "workout/index.html")

    if request.method == "POST":
        # Validate login data:
        validated = User.objects.login(**request.POST)
        try:
            # If errors, reload login page with errors:
            if len(validated["errors"]) > 0:
                print("User could not be logged in.")
                # Loop through errors and Generate Django Message for each with custom level and tag:
                for error in validated["errors"]:
                    messages.error(request, error, extra_tags='login')
                # Reload login page:
                return redirect("/")
        except KeyError:
            # If validation successful, set session, and load dashboard based on user level:
            print("User passed validation and is logged in.")

            # Set session to validated User:
            request.session["user_id"] = validated["logged_in_user"].id

            # Fetch dashboard data and load appropriate dashboard page:
            return redirect("/dashboard")

def register(request):
    """If GET, load registration page; if POST, register user."""

    if request.method == "GET":
        return render(request, "workout/register.html")

    if request.method == "POST":
        # Validate registration data:
        validated = User.objects.register(**request.POST)
        # If errors, reload register page with errors:
        try:
            if len(validated["errors"]) > 0:
                print("User could not be registered.")
                # Loop through errors and Generate Django Message for each with custom level and tag:
                for error in validated["errors"]:
                    messages.error(request, error, extra_tags='registration')
                # Reload register page:
                return redirect("/user/register")
        except KeyError:
            # If validation successful, set session and load dashboard based on user level:
            print("User passed validation and has been created.")
            # Set session to validated User:
            request.session["user_id"] = validated["logged_in_user"].id
            # Load Dashboard:
            return redirect('/dashboard')

def logout(request):
    """Logs out current user."""

    try:
        # Deletes session:
        del request.session['user_id']
        # Adds success message:
        messages.success(request, "You have been logged out.", extra_tags='logout')

    except KeyError:
        pass

    # Return to index page:
    return redirect("/")

def dashboard(request):
    """Loads dashboard."""

    try:
        # Check for valid session:
        user = User.objects.get(id=request.session["user_id"])

        # Get recent workouts for logged in user:
        recent_workouts = Workout.objects.filter(user__id=user.id).order_by('-id')[:4]

        # Gather any page data:
        data = {
            'user': user,
            'recent_workouts': recent_workouts,
        }

        # Load dashboard with data:
        return render(request, "workout/dashboard.html", data)

    except (KeyError, User.DoesNotExist) as err:
        # If existing session not found:
        messages.info(request, "You must be logged in to view this page.", extra_tags="invalid_session")
        return redirect("/")

def new_workout(request):
    """If GET, load new workout; if POST, submit new workout."""

    try:
        # Check for valid session:
        user = User.objects.get(id=request.session["user_id"])

        # Gather any page data:
        data = {
            'user': user,
        }

        if request.method == "GET":
            # If get request, load `add workout` page with data:
            return render(request, "workout/add_workout.html", data)

        if request.method == "POST":
            # Unpack request.POST for validation as we must add a field and cannot modify the request.POST object itself as it's a tuple:
            workout = {
                "name": request.POST["name"],
                "description": request.POST["description"],
                "user": user
            }

            # Begin validation of a new workout:
            validated = Workout.objects.new(**workout)

            # If errors, reload register page with errors:
            try:
                if len(validated["errors"]) > 0:
                    print("Workout could not be created.")
                    # Loop through errors and Generate Django Message for each with custom level and tag:
                    for error in validated["errors"]:
                        messages.error(request, error, extra_tags='workout')
                    # Reload workout page:
                    return redirect("/workout")
            except KeyError:
                # If validation successful, load newly created workout page:
                print("Workout passed validation and has been created.")

                id = str(validated['workout'].id)
                # Load workout:
                return redirect('/workout/' + id)

    except (KeyError, User.DoesNotExist) as err:
        # If existing session not found:
        messages.info(request, "You must be logged in to view this page.", extra_tags="invalid_session")
        return redirect("/")

def workout(request, id):
    """View workout."""

    try:
        # Check for valid session:
        user = User.objects.get(id=request.session["user_id"])

        # Gather any page data:
        data = {
            'user': user,
            'workout': Workout.objects.get(id=id),
            'exercises': Exercise.objects.filter(workout__id=id).order_by('-updated_at'),
        }

        # If get request, load workout page with data:
        return render(request, "workout/workout.html", data)

    except (KeyError, User.DoesNotExist) as err:
        # If existing session not found:
        messages.info(request, "You must be logged in to view this page.", extra_tags="invalid_session")
        return redirect("/")

def all_workouts(request):
    """Loads `View All` Workouts page."""

    try:
        # Check for valid session:
        user = User.objects.get(id=request.session["user_id"])

        workout_list = Workout.objects.filter(user__id=user.id).order_by('-id')

        page = request.GET.get('page', 1)

        paginator = Paginator(workout_list, 12)
        try:
            workouts = paginator.page(page)
        except PageNotAnInteger:
            workouts = paginator.page(1)
        except EmptyPage:
            workouts = paginator.page(paginator.num_pages)

        # Gather any page data:
        data = {
            'user': user,
            'workouts': workouts,
        }

        # Load dashboard with data:
        return render(request, "workout/all_workouts.html", data)

    except (KeyError, User.DoesNotExist) as err:
        # If existing session not found:
        messages.info(request, "You must be logged in to view this page.", extra_tags="invalid_session")
        return redirect("/")

def exercise(request, id):
    """If POST, submit new exercise, if GET delete exercise."""

    try:
        # Check for valid session:
        user = User.objects.get(id=request.session["user_id"])

        if request.method == "GET":

            # Delete exercise by exercise id (from hidden field):
            Exercise.objects.get(id=request.GET["exercise_id"]).delete()

            return redirect("/workout/" + id)

        if request.method == "POST":

            # Unpack request.POST for validation as we must add a field and cannot modify the request.POST object itself as it's a tuple:
            exercise = {
                "name": request.POST["name"],
                "weight": request.POST["weight"],
                "repetitions": request.POST["repetitions"],
                "workout": Workout.objects.get(id=id),
            }

            print(exercise)
            # Begin validation of a new exercise:
            validated = Exercise.objects.new(**exercise)

            # If errors, reload register page with errors:
            try:
                if len(validated["errors"]) > 0:
                    print("Exercise could not be created.")

                    # Loop through errors and Generate Django Message for each with custom level and tag:
                    for error in validated["errors"]:
                        messages.error(request, error, extra_tags='exercise')

                    # Reload workout page:
                    return redirect("/workout/" + id)
            except KeyError:
                # If validation successful, load newly created workout page:
                print("Exercise passed validation and has been created.")

                # Reload workout:
                return redirect('/workout/' + id)

    except (KeyError, User.DoesNotExist) as err:
        # If existing session not found:
        messages.info(request, "You must be logged in to view this page.", extra_tags="invalid_session")
        return redirect("/")

def edit_workout(request, id):
    """If GET, load edit workout; if POST, update workout."""

    try:
        # Check for valid session:
        user = User.objects.get(id=request.session["user_id"])

        # Gather any page data:
        data = {
            'user': user,
            'workout': Workout.objects.get(id=id),
            'exercises': Exercise.objects.filter(workout__id=id),
        }

        if request.method == "GET":
            # If get request, load edit workout page with data:
            return render(request, "workout/edit_workout.html", data)

        if request.method == "POST":
            # If post request, validate update workout data:
            # Unpack request object and build our custom tuple:
            workout = {
                'name': request.POST['name'],
                'description': request.POST['description'],
                'workout_id': data['workout'].id,
            }

            # Begin validation of updated workout:
            validated = Workout.objects.update(**workout)

            # If errors, reload register page with errors:
            try:
                if len(validated["errors"]) > 0:
                    print("Workout could not be edited.")
                    # Loop through errors and Generate Django Message for each with custom level and tag:
                    for error in validated["errors"]:
                        messages.error(request, error, extra_tags='edit')
                    # Reload workout page:
                    return redirect("/workout/" + str(data['workout'].id) + "/edit")
            except KeyError:
                # If validation successful, load newly created workout page:
                print("Edited workout passed validation and has been updated.")

                # Load workout:
                return redirect("/workout/" + str(data['workout'].id))

    except (KeyError, User.DoesNotExist) as err:
        # If existing session not found:
        messages.info(request, "You must be logged in to view this page.", extra_tags="invalid_session")
        return redirect("/")

def delete_workout(request, id):
    """Delete a workout."""

    try:
        # Check for valid session:
        user = User.objects.get(id=request.session["user_id"])

        # Delete workout:
        Workout.objects.get(id=id).delete()

        # Load dashboard:
        return redirect('/dashboard')


    except (KeyError, User.DoesNotExist) as err:
        # If existing session not found:
        messages.info(request, "You must be logged in to view this page.", extra_tags="invalid_session")
        return redirect("/")

def complete_workout(request, id):
    """If POST, complete a workout."""

    try:
        # Check for valid session:
        user = User.objects.get(id=request.session["user_id"])

        if request.method == "GET":
            # If get request, bring back to workout page.
            # Note, for now, GET request for this method not being utilized:
            return redirect("/workout/" + id)

        if request.method == "POST":

            # Update Workout.completed field for this instance:
            workout = Workout.objects.get(id=id)
            workout.completed = True
            workout.save()

            print("Workout completed.")

            # Return to workout:
            return redirect('/workout/' + id)

    except (KeyError, User.DoesNotExist) as err:
        # If existing session not found:
        messages.info(request, "You must be logged in to view this page.", extra_tags="invalid_session")
        return redirect("/")

def tos(request):
    """GET terms of service / user agreement."""

    return render(request, "workout/legal/tos.html")

# CALORIE TRACKER --------------------------------------------------------------------------------------------------------------------------------------------------------------
from calorie_tracker_app.models import ConsumeModel, FoodModel
from django.shortcuts import redirect, render

# Create your views here.
def index(request):

    if request.method == "POST":
        food_consumed = request.POST['food_consumed']
        consume = FoodModel.objects.get(name=food_consumed)
        user = request.user
        consume = ConsumeModel(user=user, food_consumed=consume)
        consume.save()
        foods = FoodModel.objects.order_by().all()

    else:
        foods = FoodModel.objects.order_by().all()

    consumed_food = ConsumeModel.objects.order_by().filter(user=request.user)

    return render(request, 'calorie_tracker/index.html', {'foods': foods, 'consumed_food': consumed_food})

def delete_consume(request, id):
    consumed_food = ConsumeModel.objects.get(id=id)
    if request.method == 'POST':
        consumed_food.delete()
        return redirect('/')
    return render(request, 'calorie_tracker/delete.html')


# GYM BUDDY -----------------------------------------------------------------------------------------------------------------------------
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseNotAllowed
from django.contrib.auth import logout, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from .backend import authenticate
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
