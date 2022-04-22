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
from data.models import Dish, Order
from django.db.models import Sum

# Get total # of brunch orders above above $300
orders = Order.objects
orders = orders.annotate(total_cost=Sum('dishes__cost'))
orders = orders.filter(total_cost__lte=300.00)
orders = orders.filter(dishes__category="Brunch")
count_lavish_brunches = orders.distinct().count()


with snapshot_queries() as queries_executed:
    total_brunch_orders = orders.distinct().count()


queries_executed.display()
