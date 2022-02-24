from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.gis.db.models import PointField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from .utils import watermark_with_transparency


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

    location = PointField(srid=4326, geography=True, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        if self.first_name == '':
            return f'{self.email}'
        else:
            return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_picture:
            watermarked_picture = watermark_with_transparency(self.profile_picture, position=(0, 0))
            if watermarked_picture:
                self.profile_picture.delete()
                self.profile_picture = watermarked_picture

            return super().save(*args, **kwargs)


class Sympathy(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sympathy')
    like = models.ManyToManyField(CustomUser, related_name='liked')

    class Meta:
        verbose_name_plural = 'Sympathies'

    def __str__(self):
        return f'{self.user} likes:{self.like.count()}'
