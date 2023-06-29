from django.shortcuts import render, redirect
from django.contrib import messages # access django's `messages` module.
from .models import Workout, Exercise
from webapp.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
import csv



def dashboard(request):
    """Loads dashboard."""

    try:
        # Check for valid session:

        user = User.objects.get(id = request.user.id)

        # Get recent workouts for logged in user:
        recent_workouts = Workout.objects.filter(user__id=user.id).order_by('-id')[:4]

        # Gather any page data:
        data = {
            'user': user,
            'recent_workouts': recent_workouts,
        }

        # Load dashboard with data:
        return render(request, "workout_tracker/dashboard.html", data)

    except (KeyError, User.DoesNotExist) as err:
        # If existing session not found:
        messages.info(request, "You must be logged in to view this page.", extra_tags="invalid_session")
        return redirect("workout-tracker")

def new_workout(request):
    """If GET, load new workout; if POST, submit new workout."""



    try:
        # Check for valid session:
        user = User.objects.get(id=request.user.id)

        # Gather any page data:
        data = {
            'user': user,
        }

        if request.method == "GET":
            # If get request, load `add workout` page with data:
            return render(request, "workout_tracker/add_workout.html", data)

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
                    return redirect("/workout-tracker/")

            except KeyError:
                # If validation successful, load newly created workout page:
                print("Workout passed validation and has been created.")

                id = str(validated['workout'].name)
                data = []
                field_names = ['date', 'time', 'workout1','workout2','workout3','workout4','workout5','workout6']
                date = datetime.datetime.now().date()
                time = datetime.datetime.now().time()
                consumed_food = Workout.objects.order_by().filter(user=request.user)
                print(consumed_food)
                workout1_present = 0  # set to 0 if 'workout1' is not present
                workout2_present = 0  # set to 0 if 'workout2' is not present
                workout3_present = 0  # set to 0 if 'workout3' is not present
                workout4_present = 0  # set to 0 if 'workout4' is not present
                workout5_present = 0  # set to 0 if 'workout5' is not present
                workout6_present = 0  # set to 0 if 'workout6' is not present
                if(id=='workout1'):
                    workout1_present=1
                elif(id=='workout2'):
                    workout2_present=1
                elif(id=='workout3'):
                    workout3_present=1
                elif(id=='workout4'):
                    workout4_present=1
                elif(id=='workout5'):
                    workout5_present=1
                elif(id=='workout6'):
                    workout6_present=1                


                progress = {'date': date, 'time': time, 'workout1':workout1_present ,'workout2':workout2_present,'workout3':workout3_present,'workout4':workout4_present,'workout5':workout5_present,'workout6':workout6_present}
                data.append(progress)
                print(data)

                with open('workout_tracker/workout.csv', 'a', newline='') as f_object:
                    dictwriter_object = csv.DictWriter(f_object, fieldnames=field_names)
                    dictwriter_object.writerow(progress)
                                #Load workout:

                return redirect('/workout-tracker/')

    except (KeyError, User.DoesNotExist) as err:
        # If existing session not found:
        messages.info(request, "You must be logged in to view this page.", extra_tags="invalid_session")
        return redirect("workout-tracker")

def workout(request, id):
    """View workout."""

    try:
        # Check for valid session:
        user = User.objects.get(id=request.user.id)

        # Gather any page data:
        data = {
            'user': user,
            'workout': Workout.objects.get(id=id),
            'exercises': Exercise.objects.filter(workout__id=id).order_by('-updated_at'),
        }

        # If get request, load workout page with data:
        return render(request, "workout_tracker/new-workout.html", data)

    except (KeyError, User.DoesNotExist) as err:
        # If existing session not found:
        messages.info(request, "You must be logged in to view this page.", extra_tags="invalid_session")
        return redirect("workout-tracker")

def all_workouts(request):
    """Loads `View All` Workouts page."""

    try:
        # Check for valid session:
        user = User.objects.get(id=request.user.id)

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
        return render(request, "workout_tracker/all_workouts.html", data)

    except (KeyError, User.DoesNotExist) as err:
        # If existing session not found:
        messages.info(request, "You must be logged in to view this page.", extra_tags="invalid_session")
        return redirect("workout-tracker")

def exercise(request, id):
    """If POST, submit new exercise, if GET delete exercise."""

    try:
        # Check for valid session:
        user = User.objects.get(id=request.user.id)

        if request.method == "GET":

            # Delete exercise by exercise id (from hidden field):
            Exercise.objects.get(id=request.GET["exercise_id"]).delete()

            return redirect("new-workout/" + id)

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
                    return redirect("new-workout/" + id)
            except KeyError:
                # If validation successful, load newly created workout page:
                print("Exercise passed validation and has been created.")

                # Reload workout:
                return redirect('new-workout/' + id)

    except (KeyError, User.DoesNotExist) as err:
        # If existing session not found:
        messages.info(request, "You must be logged in to view this page.", extra_tags="invalid_session")
        return redirect("workout-tracker")

def edit_workout(request, id):
    """If GET, load edit workout; if POST, update workout."""

    try:
        # Check for valid session:
        user = User.objects.get(id=request.user.id)

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
                    return redirect("new-workout/" + str(data['workout'].id) + "/edit")

            except KeyError:
                # If validation successful, load newly created workout page:
                print("Edited workout passed validation and has been updated.")

                # Load workout:
                return redirect("new-workout/" + str(data['workout'].id))

    except (KeyError, User.DoesNotExist) as err:
        # If existing session not found:
        messages.info(request, "You must be logged in to view this page.", extra_tags="invalid_session")
        return redirect("workout-tracker")

def delete_workout(request, id):
    """Delete a workout."""

    try:
        # Check for valid session:
        user = User.objects.get(id=request.user.id)

        # Delete workout:
        Workout.objects.get(id=id).delete()

        # Load dashboard:
        return redirect('workout-tracker')


    except (KeyError, User.DoesNotExist) as err:
        # If existing session not found:
        messages.info(request, "You must be logged in to view this page.", extra_tags="invalid_session")
        return redirect("workout-tracker")

def complete_workout(request, id):
    """If POST, complete a workout."""

    try:
        # Check for valid session:
        user = User.objects.get(id=request.user.id)

        if request.method == "GET":
            # If get request, bring back to workout page.
            # Note, for now, GET request for this method not being utilized:
            return redirect("new-workout/" + id)

        if request.method == "POST":

            # Update Workout.completed field for this instance:
            workout = Workout.objects.get(id=id)
            workout.completed = True
            workout.save()

            print("Workout completed.")

            # Return to workout:
            return redirect('new-workout/' + id)

    except (KeyError, User.DoesNotExist) as err:
        # If existing session not found:
        messages.info(request, "You must be logged in to view this page.", extra_tags="invalid_session")
        return redirect("workout-tracker")

    return render(request, "workout-tracker/legal/tos.html")
