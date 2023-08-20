from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def ceate_user(self, phone_number: str):
        if not phone_number:
            raise ValueError("User must have an phone number")

        user = self.model(
            phone_number=self.phone_number,
        )

        user.save(using=self._db)
        return user
