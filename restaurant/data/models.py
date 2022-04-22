from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        db_table = "customer"

class Dish(models.Model):
    name = models.CharField(max_length=256)
    category = models.CharField(max_length=256)
    cost = models.DecimalField(decimal_places=4, max_digits=12)

    class Meta:
        db_table = "dish"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    dishes = models.ManyToManyField(Dish)

    class Meta:
        db_table = "order"
