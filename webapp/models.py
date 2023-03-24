from django.db import models
from django.contrib.auth.models import AbstractUser
from autoslug import AutoSlugField
from dateutil.relativedelta import relativedelta
from datetime import date

class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True, null=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone_number=models.CharField(max_length=10,blank=True, null=True)
    gender=models.CharField(max_length=20, null=True)
    email = models.EmailField()
    # slug = AutoSlugField(populate_from='name')
    # USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = []
    dob = models.DateField(max_length=8,null=True)
    # age = models.IntegerField() 
    # def __str__(self):
    #     today = date.today()
    #     delta = relativedelta(today, self.dob)
    #     return str(delta.years)
    def __str__(self) -> str:
            return self.name

