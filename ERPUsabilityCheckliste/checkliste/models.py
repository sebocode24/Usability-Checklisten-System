from django.db import models
from django.contrib.auth.models import User

class Projekt(models.Model):
    name = models.CharField(max_length=100)
    user = models.ManyToManyField(User)

    def __str__(self):
        return self.name
    
class Kategorie(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField()

    def __str__(self):
        return self.name

class Kriterien(models.Model):
    name = models.CharField(max_length=100)
    wert = models.CharField(max_length=100)
    gewichtung = models.IntegerField()
    typ = models.CharField(max_length=100)
    projekt = models.ForeignKey(Projekt, on_delete=models.CASCADE)
    kategorie = models.ForeignKey(Kategorie, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
