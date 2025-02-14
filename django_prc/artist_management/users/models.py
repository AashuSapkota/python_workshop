from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
import datetime

# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, first_name, last_name, email, password, phone, dob, gender, address, created_at, updated_at, **extra_fields):
        user = self.model(first_name=first_name, last_name=last_name, email=email, password=password,
                          phone=phone, dob=dob, gender=gender, address=address,
                          created_at=created_at, updated_at=updated_at, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, first_name, last_name, email, password, phone, dob, gender, address, created_at, updated_at, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(first_name, last_name, email, password,
                                 phone, dob, gender, address,
                                 created_at, updated_at, **extra_fields)
    
    def create_superuser(self, first_name, last_name, email, password, phone, dob, gender, address, created_at, updated_at, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(first_name, last_name, email, password,
                                 phone, dob, gender, address,
                                 created_at, updated_at, **extra_fields)    


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other')
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=500)
    phone = models.CharField(max_length=20)
    dob = models.DateTimeField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ('email',)
        verbose_name = _('user')
        verbose_name_plural = _('users')