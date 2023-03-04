from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class User(AbstractUser):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name')
    phone_number = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    email = models.EmailField()
    age = models.IntegerField(blank=False,null=False,max_length=7)
    height = models.IntegerField(blank=False,null=False,max_length=7)
    curr_wght = models.IntegerField(blank=False,null=False,max_length=7)
    tar_wght = models.IntegerField(blank=False,null=False,max_length=7)
    bmi=models.FloatField(blank=False,null=False)

    def __str__(self) -> str:
        return self.name


