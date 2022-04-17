import snapshot_queries.optional_dependencies


def default_query_filter(query: str):
    if snapshot_queries.optional_dependencies.DJANGO_INSTALLED:
        # Exclude SAVEPOINT and any query on `django_content_type` that does NOT involve a
        # join. The content type queries are unpredictable due to Django's caching and
        # often cause flakiness in tests.
        return ("SAVEPOINT" not in query) and (
            "JOIN" in query or "django_content_type" not in query
        )

    else:
        return True
