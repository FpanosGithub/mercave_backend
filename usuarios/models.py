from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Usuario(AbstractUser):
    telefono = models.CharField(max_length=10, null= True, blank = True)
    puesto = models.CharField(max_length=40, null= True, blank = True)
    pass