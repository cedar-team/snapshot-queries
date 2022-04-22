from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=256)


class Dishes(models.Model):
    category = models.CharField(max_length=256)
    cost = models.DecimalField(decimal_places=4, max_digits=12)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    dishes = models.ManyToManyField(Dishes)
