from calorie_tracker_app.models import ConsumeModel, FoodModel
from django.shortcuts import redirect, render

# Create your views here.
def calorie_tracker(request):

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

    return render(request, 'calorie_tracker_app/index.html', {'foods': foods, 'consumed_food': consumed_food})

def delete_consume(request, id):
    consumed_food = ConsumeModel.objects.get(id=id)
    if request.method == 'POST':
        consumed_food.delete()
        return redirect('/calorie-tracker/')
    return render(request, 'calorie_tracker_app/delete.html')