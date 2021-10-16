from django.db import models


# Create your models here.
class Register(models.Model):
    first_name = models.CharField(max_length=90)
    last_name = models.CharField(max_length=90)
    username = models.CharField(max_length=90)
    email = models.EmailField(max_length=90)
    password = models.CharField(max_length=45)


class HousingData(models.Model):
    area = models.IntegerField()
    bhk = models.IntegerField()
    parking = models.IntegerField()
    furnishing = models.IntegerField()
    transaction = models.IntegerField()
