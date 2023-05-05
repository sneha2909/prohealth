from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import numpy as np
from .models import User
from django.contrib import messages
from .models import User_Info, User_Exercise_Info, Playlist_Check, Diet_Menu
import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import StandardScaler
import pickle
from scipy.optimize import differential_evolution
from calorie_tracker_app.models import FoodModel


#food recommendations
import random
from pandas import DataFrame
# Create your views here.


workouts = {
    'workout1' : ('Squats', 'Push-ups', 'Lunges', 'Pull-ups', 'Plank', 'Burpees'),
    'workout2' : ('Deadlifts', 'Bench Press', 'Bent-Over Rows', 'Overhead Press', 'Squats'),
    'workout3' : ('Jumping Jacks', 'Mountain Climbers', 'Kettlebell Swings', 'Box Jumps', 'Battle Ropes', 'Rowing Machine Sprints'),
    'workout4': ('Burpees', 'Dumbbell thrusters', 'Kettlebell Swings', 'Pull-ups', 'Push-ups'),
    'workout5': ('Leg Press', 'Lat Pulldown', 'Leg Extension', 'Cable Curl', 'Bench Press'),
    'workout6': ('Jump Squats', 'Medicine ball slams', 'Plank jacks', 'Push-ups', 'Battle Ropes', 'Rowing Machine Sprints')
}

def load_food():
    food_data = pd.read_csv("webapp/indian_meal.csv")
    for index, row in food_data.iterrows():
        model = FoodModel()
        model.name = row['Meal']
        model.carbs = row['Carbohydrates']
        model.protein = row['Protein']
        model.fats = row['Fats']
        model.calories = row['Calories']
        model.save()


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
        
        if not FoodModel.objects.order_by().all().exists(): 
            load_food()
            
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
        if not FoodModel.objects.order_by().all().exists():
            load_food()
        # load_model()
    else:
        print("User is not logged in :(")
    return render(request, 'webapp/home.html', {'user': request.user})


def logout_view(request):
    logout(request)
    return redirect('home')

# def scaler(new_data):
#     # Load the saved scaler from the pickle file
#     with open('webapp/scaler.pkl', 'rb') as f:
#         scaler = pickle.load(f)

#     new_data_scaled = scaler.transform(new_data)
#     return new_data_scaled


def readcsv(path):
    data = pd.read_csv(path)
    return data


def pre_process(raw):
    non_features = ['weight', 'change']
    data = raw.dropna()
    X = data.drop(columns=non_features)
    exercises = X.columns.tolist()[1:]
    X = X.values
    
    X = np.asarray(X).astype(np.float32)
    
    with open('webapp/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    X_scaled = scaler.transform(X)
    # print(new_data_scaled)
    return X_scaled, exercises


def de_predict(data):
    # daily_target = -0.25  # daily loss aim in ounces, approx 0.25kg
    # confidence_factor = 0.5
    # model = load_model('webapp/my_model.h5')
    # X = data.copy()
    # for i in range(1, len(X)):
    #     X[i] = np.round(X[i])
    # scaler = pickle.load(open('webapp/scaler.pkl', 'rb'))
    # X_scaled = scaler.transform(X.reshape(1, -1))
    # return np.abs(model.predict(X_scaled) - daily_target/confidence_factor)
    daily_target = -0.25  # daily loss aim in ounces, approx 0.25kg
    confidence_factor = 0.5
    model = load_model('webapp/my_model.h5')
    z = data.copy()
    for i in range(1, len(data)):
        z[i] = np.round(data[i])
    z_2d = z.reshape(1, -1)
    scaler = pickle.load(open('webapp/scaler.pkl', 'rb'))
    z_scaled = scaler.transform(z_2d)
    return np.abs(model.predict(z_scaled) - daily_target/confidence_factor)

def recommend_exercise(calorie, exercises, data):
    bounds = [(calorie, calorie+1)] + len(exercises)*[(0, 1)]
    result = differential_evolution(de_predict, bounds=bounds)
    recommended_exercises = [(exercise, recommend)
                             for recommend, exercise in zip(result.x[1:], exercises)]
    recommended_exercises.sort(reverse=True, key=lambda x: x[1])
    top_recommendation = recommended_exercises[0][0] if recommended_exercises[0][1] > 0.5 else 'Rest day'
    return top_recommendation

@login_required
def dashboard(request):
    raw = readcsv('webapp/health.csv')
    print(raw.head())
    X_scaled, exercises = pre_process(raw)
    menu = readcsv('webapp/sample_menu.csv')
    # model = load_model('webapp/my_model.h5')
    menu['recommended_exercise'] = menu['calories'].apply(
        lambda x: recommend_exercise(x, exercises, X_scaled))

    recommendation = menu['recommended_exercise'][0]
    print(recommendation)
    exercise_list = workouts[str(recommendation)]
    context = {
        'workout_name' : str(recommendation),
        'exercises': exercise_list
    }
    return render(request, 'webapp/workout_dashboard.html', context)


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

    
def weeklyCalories():
    # Calorie Calculator

    # BMR formula for males: 10 x weight (kg) + 6.25 x height (cm) - 5 x age (years) + 5
    # BMR formula for females: 10 x weight (kg) + 6.25 x height (cm) - 5 x age (years) - 161

    # Activity level multiplier:
    # Sedentary (little or no exercise) = 1.2
    # Lightly active (light exercise or sports 1-3 days a week) = 1.375
    # Moderately active (moderate exercise or sports 3-5 days a week) = 1.55
    # Very active (hard exercise or sports 6-7 days a week) = 1.725
    # Extra active (very hard exercise or sports, physical job or training twice a day) = 1.9


    # Input user information
    age = int(input("Enter your age: "))
    sex = input("Enter your sex (M/F): ")
    weight = float(input("Enter your weight in kilograms: "))
    height = float(input("Enter your height in centimeters: "))
    activity_level = input(
        "Enter your activity level (Sedentary/Lightly active/Moderately active/Very active/Extra active): ")

    # Calculate BMR based on sex
    if sex == "M":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # Calculate total calorie needs based on activity level
    if activity_level == "Sedentary":
        calorie_needs = bmr * 1.2
    elif activity_level == "Lightly active":
        calorie_needs = bmr * 1.375
    elif activity_level == "Moderately active":
        calorie_needs = bmr * 1.55
    elif activity_level == "Very active":
        calorie_needs = bmr * 1.725
    else:
        calorie_needs = bmr * 1.9

    # Print out estimated calorie needs
    print("Your estimated daily calorie needs are: ", calorie_needs)
    return calorie_needs

def genetic(data):
    weeklyCalories = 1500 * 7
    
    populationSize = 50
    food = data['Food']
    calories = data['Calories']
    utility = data['Utility']
    carbo = data['Carbohydrate']
    fat = data['Fat']
    protein = data['Protein']


    numberOfGenerations = 100
    rateOfMutation = 0.1
    tournamentSize = 10

    currentGen = []
    currentBestSolution = []
    highestScoreList = []
    averageScoreList = []

    # Initialise a Population
    listofones = [1]*21
    listofzeros = [0]*(len(food)-21)

    for i in range(populationSize):
        currentGen.append(listofones + listofzeros)
        random.shuffle(currentGen[i])
        
    for g in range(numberOfGenerations):
        # initializes two arrays with populationSize number of elements, all of which are initially set to 0.
        fitnessScore = [0]*populationSize
        normalisedFitnessScore = [0]*populationSize
        totalPolulationFitnessScore = 0
        highestScore = 0
        nextGen = []
        newGen = []

        # Perform Evaluation of Fitness Score
        for i in range(populationSize):
            totalCalories = 0
            for j in range(len(food)):
                # This loop calculates the fitness score for a solution and the total calories in the solution.
                fitnessScore[i] += currentGen[i][j] * utility[j]
                totalCalories += currentGen[i][j] * calories[j]
            if totalCalories > weeklyCalories:
                # checks if the total calories in the solution exceed the weekly calories required and adjusts the fitness score accordingly.
                fitnessScore[i] += weeklyCalories - totalCalories
            if fitnessScore[i] > highestScore:
                currentBestSolutionIndex = i
                # checks if the current solution has the highest fitness score, and if so, sets the index and score for the best solution.
                highestScore = fitnessScore[i]

            # adds the fitness score of the current solution to the total population fitness score.
            totalPolulationFitnessScore += fitnessScore[i]
            # Total population fitness score is the sum of fitness scores of all individuals in the population.
            # It is used to compute the normalized fitness scores, which are the relative probabilities of selecting each individual for reproduction.

        highestScoreList.append(highestScore)
        averageScoreList.append(totalPolulationFitnessScore/populationSize)
        currentBestSolution = currentGen[currentBestSolutionIndex].copy()

        for i in range(populationSize):
            # calculates the normalized fitness score for each solution in the current generation.
            normalisedFitnessScore[i] = fitnessScore[i]/totalPolulationFitnessScore

        # Perform Selection
        for i in range(populationSize):
            cumulativeNormalisedFitnessScore = 0
            # Initialize variables for roulette wheel selection.
            rwScore = random.uniform(0, 1)
            for j in range(populationSize):
                cumulativeNormalisedFitnessScore += normalisedFitnessScore[j]
                if cumulativeNormalisedFitnessScore >= rwScore:
                    nextGen.append(currentGen[j].copy())
                    # performs roulette wheel selection to select the next generation.
                    break

        # Perform Mutation
        for i in range(populationSize):
            for j in range(len(food)):
                if rateOfMutation > random.uniform(0, 1):
                    # If the rate of mutation is higher than this random number,
                    nextGen[i][j] = abs(nextGen[i][j] - 1)
                    # then the gene (represented by the value of nextGen[i][j]) at position j in individual i of the next generation (nextGen) is mutated.
                    # The mutation operator in this code flips the value of the gene (from 0 to 1 or 1 to 0) by subtracting the current value of the gene from 1 using the abs function.
                    # This operation ensures that the value of the gene is flipped regardless of its current value.
        # Adjust bits back to zero
        for i in range(populationSize):
            # For each individual in the population, the code calculates the number of bits that need to be adjusted (i.e., flipped from 1 to 0 or vice versa) to ensure that there are exactly 21 bits that are equal to 1 in the solution.
            bitsToAdjust = sum(nextGen[i]) - 21

            if bitsToAdjust > 0:  # If there are too many bits that are equal to 1, the code randomly selects bits that are equal to 1 and flips them to 0 until there are exactly 21 bits that are equal to 1.
                # If there are too few bits that are equal to 1, the code randomly selects bits that are equal to 0 and flips them to 1 until there are exactly 21 bits that are equal to 1.
                for j in range(bitsToAdjust):
                    index = random.randint(0, len(food)-1)
                    notFound = True
                    while notFound:
                        if nextGen[i][index] == 1:
                            nextGen[i][index] = 0
                            notFound = False
                        else:
                            index += 1
                            index = index % len(food)
            elif bitsToAdjust < 0:
                for j in range(abs(bitsToAdjust)):
                    index = random.randint(0, len(food)-1)
                    notFound = True
                    while notFound:
                        if nextGen[i][index] == 0:
                            nextGen[i][index] = 1
                            notFound = False
                        else:
                            # This process ensures that the solutions in the population remain valid and consistent with the problem constraints. After adjusting the bits, the code proceeds to form a new generation by using an N-tournament selection process.
                            index += 1
                            index = index % len(food)

                            # Form a new Generation by using N-tournament. Randomly draw N parents and N offspring and select the best for new generation

        # Compute fitness score for offspring
        fitnessScore2 = [0]*populationSize
        for i in range(populationSize):
            totalCalories = 0
            for j in range(len(food)):
                fitnessScore2[i] += nextGen[i][j] * utility[j]
                totalCalories += nextGen[i][j] * calories[j]
            if totalCalories > weeklyCalories:
                fitnessScore2[i] += weeklyCalories - totalCalories

        for i in range(populationSize):

            highest_fitness_score = 0
            index = 0
            parent_selected = True

            for j in range(tournamentSize):
                index_p = int(random.uniform(0, populationSize-1))
                index_o = int(random.uniform(0, populationSize-1))

                if highest_fitness_score < fitnessScore[index_p]:
                    parent_selected = True
                    index = index_p
                    highest_fitness_score = fitnessScore[index_p]

                if highest_fitness_score < fitnessScore2[index_o]:
                    parent_selected = False
                    index = index_o
                    highest_fitness_score = fitnessScore[index_o]

            # For each individual in the new generation, the code randomly selects N parents and N offspring, and selects the one with the highest fitness score (i.e., highest utility score while keeping the total calories under the weekly limit).
            if parent_selected:
                newGen.append(currentGen[index].copy())
            else:
                newGen.append(nextGen[index].copy())

        currentGen = newGen.copy()

        # Reduce rate of Mutation as search progresses
        # The code then updates the current generation with the new generation and reduces the mutation rate as the search progresses. Specifically, if the current generation is a multiple of 10% of the total number of generations, the mutation rate is reduced by a factor of 0.9.
        if (g+1) % (numberOfGenerations/10) == 0:
            rateOfMutation *= 0.9
            
    print("Highest Fitness Score:", highestScore)
    print("Average Polulation Fitness Score:", totalPolulationFitnessScore/populationSize)
    print("Total Polulation Fitness Score:", totalPolulationFitnessScore)
    
    return currentBestSolution


def diet_recommend(request):
    totalcalories = 0
    data = readcsv("webapp/indian_meal_increased.csv")
    food = data['Food']
    recommended_food = []
    calories = data['Calories']
    currentBestSolution = genetic(data)
    
    print("Recommended Menu for the week:\n")
    
    for i in range(len(food)):
        if currentBestSolution[i] == 1:
            totalcalories += calories[i]
            print(food[i])
            recommended_food.append(food[i])

    context = {
        'recommended_food': recommended_food
    }

    print("\nAverage Daily Calories:", totalcalories/7)
    return render(request, 'webapp/diet-recommendation.html', context)


