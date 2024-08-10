from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'Br8O63lv+,75B!Y6FqdU~sNpJEw5LsZ97?lYMHRnMBe(FrR*lel~WeS<1lI0#LgYxRgH8yJ7!02a)z-(9CseSaso4qq8t&?s,v.d4(hIDFO.^F!W==KNp77eRBl8&z&<'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass
