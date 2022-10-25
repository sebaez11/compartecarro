"""
With these settings, tests run faster.
"""

from .base import *  # noqa
from .base import env

# GENERAL
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="vdsWK7tYb774wCAXPQfPA5XVe0VKbMHvFUYAxNh8GzWNglxXmgl4ePLdI9FIcw21",
)
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# PASSWORDS
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# EMAIL
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# DEBUGING FOR TEMPLATES
TEMPLATES[0]["OPTIONS"]["debug"] = True  # type: ignore # noqa F405


