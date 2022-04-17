SQLALCHEMY_INSTALLED = False
try:
    import sqlalchemy  # noqa
except ImportError:
    pass
else:
    SQLALCHEMY_INSTALLED = True


DJANGO_INSTALLED = False
try:
    import django  # noqa
except ImportError:
    pass
else:
    DJANGO_INSTALLED = True
