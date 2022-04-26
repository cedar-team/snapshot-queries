# fmt: off

# https://carbon.now.sh/2fZ0TfckDaQsXeYCbE2k

import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

os.environ["DJANGO_SETTINGS_MODULE"] = "restaurant.settings"

import django

django.setup()


from snapshot_queries import snapshot_queries
from data.models import Dish, Order, Customer
from django.db.models import Sum, Count

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


def favorite_dish(customer_name):
    customer_dishes = Dish.objects.filter(order__customer__name='Juan')

    return customer_dishes.annotate(count=Count('name')).order_by('count').last()

with snapshot_queries() as queries_executed:
    favorite_dish("Juan")

queries_executed.display()




