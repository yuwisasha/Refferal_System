from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest

from .models import User, SMSCode


class SMSBackend(BaseBackend):
    def authenticate(
        self,
        request: HttpRequest,
        phone_number: str = None,
        code: str = None,
        **kwargs
    ) -> User | None:
        sended_codes = [
            *SMSCode.objects.filter(phone_number=phone_number).values_list(
                "code", flat=True
            )
        ]

        if code in sended_codes:
            try:
                user = User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                user = User.objects.create(phone_number=phone_number)
        else:
            return None

        SMSCode.objects.all().filter(phone_number=phone_number).delete()
        return user

    def get_user(self, user_id) -> User | None:
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
