from django.db import models
from django.contrib.auth.models import AbstractUser

# # Create your models here.
class User(AbstractUser):
    address = models.TextField(max_length=200, blank=True)
    token = models.CharField(max_length=200, blank=True)