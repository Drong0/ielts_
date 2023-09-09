from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager


class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """

    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value


class Role(models.Model):
    objects = None

    class Name(models.TextChoices):
        ADMIN = 'admin', _('Admin')
        STUDENT = 'student', _('Student')

    name = models.CharField(max_length=15, choices=Name.choices, default=Name.STUDENT)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = LowercaseEmailField(unique=True)
    email_approved = models.BooleanField(default=False)
    phone = PhoneNumberField(unique=True, blank=True)
    role = models.ForeignKey('Role', on_delete=models.PROTECT, related_name='role', blank=True, default='', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(
        _('active'),
        default=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
