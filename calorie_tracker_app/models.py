from django.db.models import Model, ForeignKey, CASCADE
from django.db.models.fields import (CharField, FloatField, IntegerField)
from django.contrib.auth import get_user_model
User = get_user_model()

 #Create your models here.
class FoodModel(Model):
    
    name = CharField(("Food"),max_length=255)
    calories = IntegerField(("Calories"),max_length=255)
    carbs = FloatField(("Carbohydrate"),max_length=255)
    fats = FloatField(("Fat"),max_length=255)
    protein = FloatField(("Protein"),max_length=255)
    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Food'
        verbose_name_plural = 'Foods'
        
class ConsumeModel(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    food_consumed = ForeignKey(FoodModel, on_delete=CASCADE)

    def __str__(self):
        return f'{self.user.username} {self.food_consumed.name}'

    class Meta:
        verbose_name = 'Consume'
        verbose_name_plural = 'Consumes'
