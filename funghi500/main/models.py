from django.db import models

# Create your models here.
class Valore(models.Model):
    pass

class Mese(models.Model):
    pass

class Fungo(models.Model):
    diametroMIN = models.IntegerField()
    diametroMAX = models.IntegerField()
    altezzaMIN = models.IntegerField()
    altezzaMAX = models.IntegerField()
    altitudineMIN = models.IntegerField()
    altitudineMAX = models.IntegerField()
    mesi = models.ManyToManyField(Mese, related_name='funghi')
    valori = models.ManyToManyField(Valore, related_name='funghi')