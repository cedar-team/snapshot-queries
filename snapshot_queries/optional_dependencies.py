SQLALCHEMY_INSTALLED = False
try:
    import sqlalchemy
except ImportError:
    pass
else:
    SQLALCHEMY_INSTALLED = True


DJANGO_INSTALLED = False
try:
    import django
except ImportError:
    pass
else:
    DJANGO_INSTALLED = True
