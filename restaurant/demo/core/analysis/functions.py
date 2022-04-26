from data.models import *
from snapshot_queries import *
from django.db.models import Count


def favorite_dish(customer_name):
    [d.delete() for d in Dish.objects.all()]
    [c.delete() for c in Customer.objects.all()]
    [o.delete() for o in Order.objects.all()]

    lobster, _ = Dish.objects.get_or_create(name="Lobster", category="Dinner", cost=100)
    caviar, _ = Dish.objects.get_or_create(name="Caviar", category="Dinner", cost=100)
    truffles, _ = Dish.objects.get_or_create(name="Truffles", category="Dinner", cost=100)
    kobe_beef, _ = Dish.objects.get_or_create(name="Kobe Beef", category="Dinner", cost=100)
    juan, _ = Customer.objects.get_or_create(name="Juan")

    monday_order = Order.objects.create(customer=juan)
    monday_order.dishes.add(lobster)

    tuesday_order = Order.objects.create(customer=juan)
    tuesday_order.dishes.add(caviar, lobster)

    wednesday_order = Order.objects.create(customer=juan)
    wednesday_order.dishes.add(caviar, lobster, truffles)

    customer_dishes = Dish.objects.filter(order__customer__name='Juan')

    return customer_dishes.annotate(count=Count('name')).order_by('count').last()
