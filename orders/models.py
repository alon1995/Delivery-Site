from django.db import models
from user.views import User
from main.models import Dish

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class Item(models.Model):
    dish = models.ForeignKey(Dish,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

class Delivery(models.Model):
    is_delivered = models.BooleanField(default=False)
    adress = models.CharField(max_length=100)
    comment = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    cart = models.OneToOneField(Cart,on_delete=models.CASCADE,primary_key=True)

