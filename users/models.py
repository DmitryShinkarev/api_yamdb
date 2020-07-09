from django.db import models
from django.utils.translation import ugettext_lazy
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(ugettext_lazy('email address'), unique=True)
    bio = models.TextField(blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    USER_ROLE = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )

    role = models.CharField(
        max_length=9, choices=USER_ROLE, default='user')

    objects = CustomUserManager()

    def __str__(self):
        return self.email
