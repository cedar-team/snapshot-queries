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
from django.db.models import Sum

[d.delete() for d in Dish.objects.all()]
[c.delete() for c in Customer.objects.all()]

lobster, _ = Dish.objects.get_or_create(name="Lobster", category="Dinner", cost=100)
caviar, _ = Dish.objects.get_or_create(name="Caviar", category="Dinner", cost=100)
truffles, _ = Dish.objects.get_or_create(name="Truffles", category="Dinner", cost=100)
kobe_beef, _ = Dish.objects.get_or_create(name="Kobe Beef", category="Dinner", cost=100)

for id, name in enumerate(["Alice", "Bob", "Juan"]):
    customer, _ = Customer.objects.get_or_create(name=name, id=id+1)
    order, _ = Order.objects.get_or_create(customer=customer)
    order.dishes.add(lobster)
    order.dishes.add(caviar)
    order.dishes.add(truffles)
    order.dishes.add(kobe_beef)


with snapshot_queries() as queries_executed:
    # Get the name of every customer that ordered Kobe Beef
    customers = []
    orders = Order.objects.filter(dishes__name="Kobe Beef")
    for order in orders:
        customers.append(order.customer.name)

queries_executed.display(code=False, duration=False, location=False)



with snapshot_queries() as queries_executed:
    # Get the name of every customer that ordered Kobe Beef
    customers = []
    orders = Order.objects.filter(dishes__name="Kobe Beef").select_related('customer')
    for order in orders:
        customers.append(order.customer.name)

queries_executed.display(code=False, duration=False, location=False)
