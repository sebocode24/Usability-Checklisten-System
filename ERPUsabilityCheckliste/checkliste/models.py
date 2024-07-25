from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=100)
    user = models.ManyToManyField(User)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Criterion(models.Model):
    WEIGHT_CHOICES = [
        (1, 'einfach'),
        (2, 'zweifach'),
        (3, 'dreifach'),
    ]

    RATING_CHOICES = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (0, 'Nicht relevant')
    ]
        
    name = models.CharField(max_length=100)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, null=True, blank=True)
    gewichtung = models.PositiveIntegerField(choices=WEIGHT_CHOICES, null=True, blank=True)
    projekt = models.ForeignKey(Project, on_delete=models.CASCADE)
    subkategorie = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    kategorie = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
