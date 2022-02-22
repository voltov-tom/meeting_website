from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    GENDER_CHOICES = [
        (0, 'Not selected'),
        (1, 'Male'),
        (2, 'Female')
    ]

    gender = models.IntegerField(choices=GENDER_CHOICES, default=0)
    profile_picture = models.ImageField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        if self.first_name == '':
            return f'{self.email}'
        else:
            return f'{self.first_name} {self.last_name}'
