# snapshot-queries

Capture all SQL statements executed via Django and SqlAlchemy ORM queries

Use cases

- See the exact query executed by a complex Django Queryset or SQLAlchemy query
- Quickly see the slowest queries executed in a code block
- Identify similar queries executed in a code block to help detect the N+1 query problem
- See the exact line of code that triggered a query execution, including its full stacktrace

Examples

- [Display queries executed in a code block](#display-queries-executed-in-a-code-block)
- [Display specific attributes of each query](#display-specific-attributes-of-each-query)
- [Order queries by duration](#order-queries-by-duration)
- [Inspect the slowest query](#inspect-the-slowest-query)
- [Group queries with duplicate sql statements together](#group-queries-with-duplicate-sql-statements-together)
- [Group queries with similar sql statements together](#group-queries-with-similar-sql-statements-together)

## Display queries executed in a code block

```python
from django.contrib.auth import get_user_model
from snapshot_queries import snapshot_queries

User = get_user_model()
with snapshot_queries() as queries_executed:
    User.objects.only('email').get(id=1)
    User.objects.only('email').get(id=7)

queries_executed.display()
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

## Display specific attributes of each query
You can choose which attributes to display.

Supported attributes to display:

- **code** (the python code that triggered the query)
- **duration** (how long the query took to execute)
- **idx** (the index of the query executed)
- **location**  (the location in our code where the query was executed)
- **stacktrace** (the full stacktrace for each query)
- **sql** (the sql statement of the query)
- **colored** (display the sql statement colored)
- **formatted** (display the sql statement formatted)

E.g. to display the stacktrace for each query, use `queries_executed.display(stacktrace=True)`:

```python
from django.contrib.auth import get_user_model
from snapshot_queries import snapshot_queries

User = get_user_model()

def main():
    with snapshot_queries() as queries_executed:
        User.objects.only('email').get(id=1)
        User.objects.only('is_staff').get(id=7)

    queries_executed.display(sql=True, stacktrace=True)

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

## Order queries by duration
```python
fastest_queries = queries_executed.order_by('duration')[:3]
slowest_queries = queries_executed.order_by('-duration')[:3]
slowest_queries_executed.display()
```

## Inspect the slowest query
```python
slowest_query = queries_executed.order_by('-duration')[0]
slowest_query.display(code=True, location=True, sql=True)
```

## Group queries with duplicate sql statements together
```python
from django.contrib.auth import get_user_model
from snapshot_queries import snapshot_queries

User = get_user_model()

with snapshot_queries() as queries_executed:
    User.objects.only('email').get(id=1)
    User.objects.only('email').get(id=1)
    User.objects.only('email').get(id=1)
    User.objects.only('email').get(id=7)

duplicates = queries_executed.duplicates().display()
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

## Group queries with similar sql statements together
```python
from django.contrib.auth import get_user_model
from snapshot_queries import snapshot_queries

User = get_user_model()

with snapshot_queries() as queries_executed:
    User.objects.only('email').get(id=1)
    User.objects.only('email').get(id=1)
    User.objects.only('email').get(id=1)
    User.objects.only('email').get(id=7)

similar = queries_executed.similar().display()
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
