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



with snapshot_queries() as queries_executed:
    customer = Customer.objects.create(name="Juan")

first_query = queries_executed[0]

first_query.sql       # the SQL statement for this query
first_query.code      # the Python code that triggered the query execution
first_query.duration  # how long the query took to execute

queries_executed.display()
