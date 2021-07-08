# django-snapshot-queries
Snapshot SQL in Django ORM queries. This is useful for viewing the underlying SQL that the 
Django ORM is executing. In addition, it's useful for performance. It makes N+1 queries and other query
issues easy to identify. If added to a test, code reviewers can see the exact SQL that is added.

## SnapshotQueries

A contextmanager for debugging queries executed

## Display queries executed
```python
from django.contrib.auth import get_user_model
from django_snapshot_queries import SnapshotQueries

User = get_user_model()
with SnapshotQueries() as queries:
    User.objects.only('email').get(id=1)
    User.objects.only('email').get(id=7)

queries.display()
```

Output:

```
Query 1
---------
2 ms

/path/to/module.py:5 in function_name

User.objects.only('email').get(id=1)

SELECT "auth_user"."id",
       "auth_user"."email"
FROM "auth_user"
WHERE "auth_user"."id" = 1


Query 2
---------
< 1 ms

/path/to/module.py:6 in function_name

User.objects.only('email').get(id=7)

SELECT "auth_user"."id",
       "auth_user"."email"
FROM "auth_user"
WHERE "auth_user"."id" = 7
```

### Display specific attributes of each query
You can choose which attributes to display.

Supported attributes to display:

- **code** (the python code that triggered the query)
- **duration** (how long the query took to execute)
- **idx** (the index of the query executed)
- **location**  (the location in our code where the query was executed)
- **stacktrace** (the full stacktrace for each query)
- **sql** (the sql statement of the query)

E.g. to display only the stacktrace and sql statements of each query, use `queries.display(stacktrace=True, sql=True)`:

```python
from django.contrib.auth import get_user_model
from django_snapshot_queries import SnapshotQueries

User = get_user_model()

def main():
    with SnapshotQueries() as queries:
        User.objects.only('email').get(id=1)
        User.objects.only('is_staff').get(id=7)

    queries.display(sql=True, stacktrace=True)

main()
```
Output:

```
Query 1
---------
./path/to/file.py:12 in <module>
    main()
./path/to/file.py:8 in main
    User.objects.only('email').get(id=1)

SELECT "auth_user"."id",
       "auth_user"."email"
FROM "auth_user"
WHERE "auth_user"."id" = 1


Query 2
---------
./path/to/file.py:13 in <module>
    main()
./path/to/file.py:9 in main
    User.objects.only('is_staff').get(id=7)

SELECT "auth_user"."id",
       "auth_user"."is_staff"
FROM "auth_user"
WHERE "auth_user"."id" = 7

```

### Order queries by duration
```python
fastest_queries = queries.order_by('duration')[:3]
slowest_queries = queries.order_by('-duration')[:3]
slowest_queries.display()
```

### Inspect a specific query
```python
slowest_query = queries.order_by('-duration')[0]
slowest_query.display(code=True, location=True, sql=True)
```

### Group queries with duplicate sql statements together
```python
from django.contrib.auth import get_user_model
from django_snapshot_queries import SnapshotQueries

User = get_user_model()

with SnapshotQueries() as queries:
    User.objects.only('email').get(id=1)
    User.objects.only('email').get(id=1)
    User.objects.only('email').get(id=1)
    User.objects.only('email').get(id=7)


duplicates = queries.duplicates().display()
```

Output:

```
========================
3 duplicate queries
========================
Query 1
---------
1 ms

./path/to/file.py:9 in main

User.objects.only('email').get(id=1)

SELECT "auth_user"."id",
       "auth_user"."email"
FROM "auth_user"
WHERE "auth_user"."id" = 1


Query 2
---------
< 1 ms

./path/to/file.py:10 in main

User.objects.only('email').get(id=1)

SELECT "auth_user"."id",
       "auth_user"."email"
FROM "auth_user"
WHERE "auth_user"."id" = 1


Query 3
---------
< 1 ms

./path/to/file.py:11 in main

User.objects.only('email').get(id=1)

SELECT "auth_user"."id",
       "auth_user"."email"
FROM "auth_user"
WHERE "auth_user"."id" = 1
```

### Group queries with similar sql statements together
```python
from django.contrib.auth import get_user_model
from django_snapshot_queries import SnapshotQueries

User = get_user_model()

with SnapshotQueries() as queries:
    User.objects.only('email').get(id=1)
    User.objects.only('email').get(id=1)
    User.objects.only('email').get(id=1)
    User.objects.only('email').get(id=7)


similar = queries.similar().display()
```

Output

```
========================
4 similar queries
========================
Query 1
---------
2 ms

/path/to/file.py:6 in main

User.objects.only('email').get(id=1)

SELECT "auth_user"."id",
       "auth_user"."email"
FROM "auth_user"
WHERE "auth_user"."id" = 1


Query 2
---------
< 1 ms

/path/to/file.py:7 in main

User.objects.only('email').get(id=1)

SELECT "auth_user"."id",
       "auth_user"."email"
FROM "auth_user"
WHERE "auth_user"."id" = 1


Query 3
---------
< 1 ms

/path/to/file.py:8 in main

User.objects.only('email').get(id=1)

SELECT "auth_user"."id",
       "auth_user"."email"
FROM "auth_user"
WHERE "auth_user"."id" = 1


Query 4
---------
< 1 ms

/path/to/file.py:9 in main

User.objects.only('email').get(id=7)

SELECT "auth_user"."id",
       "auth_user"."email"
FROM "auth_user"
WHERE "auth_user"."id" = 7
```
