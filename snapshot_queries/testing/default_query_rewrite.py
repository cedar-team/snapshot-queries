import re


def default_query_rewrite(query: str):
    flags = re.IGNORECASE | re.DOTALL
    query = re.sub(
        r"SELECT[\s\n](.*?)[\s\n]FROM", "SELECT ... FROM", query, flags=flags
    )
    query = re.sub(
        r"UPDATE[\s\n](.*?)[\s\\n]SET.+", r"UPDATE \1 SET ...", query, flags=flags
    )
    query = re.sub(
        r"INSERT INTO[\s\n](.*?)[\s\n]\(.*?\)",
        r"INSERT INTO \1 (...)",
        query,
        flags=flags,
    )
    # collapses snippets like `VALUES (%s, %s), (%s, %s)` to `VALUES (...)`
    query = re.sub(
        r"[(\s]VALUES\s(\((\S+(,\s+)?)+\)(,\s+)?)+",
        r" VALUES (...)",
        query,
        flags=flags,
    )
    query = re.sub(r" IN \(%s.*?\)", r" IN (...)", query, flags=flags)
    return query
