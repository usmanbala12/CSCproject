from django.db import models
from django.contrib.auth.models import User

#Create your models here.

class Bus(models.Model):
    capacity = models.IntegerField()
    name = models.CharField(max_length=15)
    model_name = models.CharField(max_length=100)
    number = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    vehicle = models.ForeignKey(Bus, on_delete=models.CASCADE)
    expiry_date = models.DateField()
    created_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.first_name + self.last_name

