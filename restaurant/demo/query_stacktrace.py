# fmt: off

# https://carbon.now.sh/2fZ0TfckDaQsXeYCbE2k

import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

os.environ["DJANGO_SETTINGS_MODULE"] = "restaurant.settings"

import django

django.setup()


from snapshot_queries import query_list, snapshot_queries
from data.models import Dish, Order, Customer
from django.db.models import Sum

from demo.core.analysis.functions import favorite_dish

with snapshot_queries() as queries_executed:
    favorite_dish("Juan")

print(queries_executed[-1].stacktrace)
