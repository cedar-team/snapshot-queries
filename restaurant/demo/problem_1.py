import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

os.environ["DJANGO_SETTINGS_MODULE"] = "restaurant.settings"

import django

django.setup()


from snapshot_queries import snapshot_queries
from data.models import Dish


with snapshot_queries() as queries_executed:
    list(
        Dish.objects.filter(order__customer__name="Juan").values_list("name", flat=True)
    )

queries_executed.display()
