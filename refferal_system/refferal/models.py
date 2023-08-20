import string

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.crypto import get_random_string

from .managers import UserManager


class User(AbstractBaseUser):
    phone_number = models.CharField(db_index=True, unique=True, max_length=10)

    personal_refferal_token = models.CharField(max_length=6, unique=True)

    invite_refferal_token = models.CharField(
        max_length=6,
        unique=False,
        blank=True,
        null=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "phone_number"

    def save(self, *args, **kwargs) -> None:
        """Generates personal refferal token when user registrated"""
        if not self.personal_refferal_token:
            while True:
                self.personal_refferal_token = get_random_string(
                    6, string.ascii_letters + string.digits
                )
                try:
                    User.objects.get(
                        personal_refferal_token=self.personal_refferal_token
                    )
                except User.DoesNotExist:
                    break

        return super().save()


class SMSCode(models.Model):
    phone_number = models.CharField(max_length=10)

    code = models.CharField(max_length=4)
