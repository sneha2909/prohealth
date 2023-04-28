from django.db import models
from django.contrib.auth.models import AbstractUser
from autoslug import AutoSlugField
from dateutil.relativedelta import relativedelta
from datetime import date

class User(AbstractUser):
    # username = models.CharField(max_length=255, unique=True, null=True)
    name = models.CharField(max_length=255)
    # password = models.CharField(max_length=255)
    phone_number=models.CharField(max_length=10,blank=True, null=True)
    gender=models.CharField(max_length=20, null=True)
    pincode=models.CharField(max_length=6,blank=True, null=True)
    location=models.CharField(max_length=30, null=True)
    email = models.EmailField()
<<<<<<< HEAD
    fav_gym_act1 = models.CharField(max_length=255, unique=True, null=True)
    fav_gym_act2 = models.CharField(max_length=255, unique=True, null=True)
=======
    # location
    # favorite gym acitivity 1
    # favorite gym acitivity 2
>>>>>>> 5ce4364a5feb1d53de1bf5398fd97573fa050fad
    # slug = AutoSlugField(populate_from='name')
    # USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = []
    dob = models.DateTimeField(null=True,blank=True)
    # age = models.IntegerField() 
    # def __str__(self):
    #     today = date.today()
    #     delta = relativedelta(today, self.dob)
    #     return str(delta.years)
    def __str__(self) -> str:
            return self.name

