import datetime
from calorie_tracker_app.models import ConsumeModel, FoodModel
from django.shortcuts import redirect, render
import pandas as pd
import csv

# Create your views here.
def calorie_tracker(request):

    if request.method == "POST":
        food_consumed = request.POST['food_consumed']
        consume = FoodModel.objects.get(name=food_consumed)
        user = request.user
        consume = ConsumeModel(user=user, food_consumed=consume)
        consume.save()
        foods = FoodModel.objects.order_by().all()
        
        data = []
        field_names = ['date', 'time', 'calories']
        calories = 0
        date = datetime.datetime.now().date()
        time = datetime.datetime.now().time()

        consumed_food = ConsumeModel.objects.order_by().filter(user=request.user)

        for food in consumed_food:
            calories += food.food_consumed.calories

        progress = {'date': date, 'time': time, 'calories': calories}
        data.append(progress)

        with open('calorie_tracker_app/calories.csv', 'a', newline='') as f_object:
            dictwriter_object = csv.DictWriter(f_object, fieldnames=field_names)
            dictwriter_object.writerow(progress)

    else:
        foods = FoodModel.objects.order_by().all()
        
    consumed_food = ConsumeModel.objects.order_by().filter(user=request.user)

    # print(calories)
    return render(request, 'calorie_tracker_app/index.html', {'foods': foods, 'consumed_food': consumed_food})

def delete_consume(request, id):
    consumed_food = ConsumeModel.objects.get(id=id)
    if request.method == 'POST':
        consumed_food.delete()
        data = []
        field_names = ['date', 'time', 'calories']
        calories = 0
        date = datetime.datetime.now().date()
        time = datetime.datetime.now().time()

        consumed_food = ConsumeModel.objects.order_by().filter(user=request.user)

        for food in consumed_food:
            calories += food.food_consumed.calories

        progress = {'date': date, 'time': time, 'calories': calories}
        data.append(progress)

        with open('calorie_tracker_app/calories.csv', 'a') as f_object:
            dictwriter_object = csv.DictWriter(f_object, fieldnames=field_names)
            dictwriter_object.writerow(progress)
            f_object.close()
        return redirect('/calorie-tracker/')
    return render(request, 'calorie_tracker_app/delete.html')