from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True, null=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.name

