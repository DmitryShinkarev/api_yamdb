from django.db import models
from django.contrib.auth.models import AbstractUser

USER_ROLES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


class User(AbstractUser):
    email = models.EmailField('email', unique=True)
    first_name = models.CharField('first name', max_length=40, blank=True)
    last_name = models.CharField('last name', max_length=40, blank=True)
    bio = models.TextField('bio', blank=True)
    role = models.CharField(max_length=9, choices=USER_ROLES, default='user')

    def __str__(self):
        return self.email
