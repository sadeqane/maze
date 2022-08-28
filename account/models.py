from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.models import UserManager


# Create your models here.


class User(AbstractUser):
    pass
