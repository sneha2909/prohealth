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
    location=models.CharField(max_length=255, null=True)
    email = models.EmailField()
    fav_gym_act1 = models.CharField(max_length=255,null=True)
    fav_gym_act2 = models.CharField(max_length=255, null=True)
    # Input user information
    age = models.CharField(max_length=3,blank=True, null=True)
    weight = models.CharField(max_length=10,blank=True, null=True)
    height = models.CharField(max_length=10,blank=True, null=True)
    activity_level = models.CharField(max_length=255,blank=True, null=True)
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

