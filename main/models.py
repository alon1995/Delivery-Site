from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
    imageUrl = models.TextField()

class Dish(models.Model):
    name = models.CharField(max_length=100,unique=True)
    price = models.IntegerField()
    description = models.TextField()
    imageUrl = models.TextField()
    is_gluten_free = models.BooleanField(default=False)
    is_vegeterian = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)




