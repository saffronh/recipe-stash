from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tags(models.Model):
    tag = models.CharField(max_length=255)

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    tags = models.ManyToManyField(Tags)

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, blank=True, null=True)
    ingredient_name = models.CharField(max_length=255)
    MEASURE_CHOICES = (
        ('CUP','cup'),
        ('TSP', 'tsp'),
        ('TBSP','tbsp'),
        ('PART','part'),
        ('PINCH','pinch'),
        ('GRAMS','grams'),
        ('ML','ml'),
        ('OZ','oz'),
        ('', ''),
    )
    measure = models.CharField(max_length=5, choices=MEASURE_CHOICES,blank=True)
    quantity = models.DecimalField(max_digits=19, decimal_places=2, blank=True)


class Method(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, blank=True, null=True)
    #step_number = models.IntegerField()
    description = models.CharField(max_length=999)
