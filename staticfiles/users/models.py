# from django.db import models
# from django.contrib.auth.models import User
#
#
# class Account(models.Model):
#     fullname = models.CharField(
#         max_length=50,
#         blank=True,
#     )
#
#     email = models.EmailField(
#         unique=True,
#     )
#
#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#     )
#
#     def __str__(self):
#         return self.email
#
#
from django.apps import apps
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin, UserManager

from django.db import models


class VentyUserManager(BaseUserManager):


    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    fullname = models.CharField(
        max_length=20,
    )

    email = models.EmailField(
        unique=True,
    )

    profile_picture = models.ImageField(
        upload_to='staticfiles',
        blank=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'email'

    objects = VentyUserManager()

    def __str__(self):
        return self.email
