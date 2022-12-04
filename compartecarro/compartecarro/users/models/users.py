# Django
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

# Utils
from compartecarro.utils.models import BaseModel


class User(BaseModel, AbstractUser):
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.'
        }
    )

    is_client = models.BooleanField(
        default=True,
        help_text=(
            'Help easily distinguish users and perform queries. '
            'Clients are the main type of user.'
        )
    )
    is_verified = models.BooleanField(default=False)

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message='Phone number must be entered in the format: +9999999999. Up to 15 digits allowed.'
    )
    phone_number = models.CharField(
        max_length=17, 
        blank=True,
        validators=[phone_regex]
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.username