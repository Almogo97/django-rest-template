from typing import TYPE_CHECKING

from django.contrib.auth.models import UserManager as DjangoUserManager

from services import mail

if TYPE_CHECKING:
    from .models import User


class UserManager(DjangoUserManager):
    def _create_user(self, email: str, password: str, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user: User = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)

        mail.send_templated_email([email], 'welcome')

        return user

    def create_user(self, email: str, password: str, **extra_fields):
        """Creates and saves a user if the given values are valid.

        Args:
            email: User's email
            password: User's password in plaintext

        Returns:
            The user instance

        Raises:
            django.core.exceptions.ValidationError: When any of the values is not valid
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields):
        """Creates and saves a superuser if the given values are valid.

        Args:
            email: User's email
            password: User's password in plaintext

        Returns:
            The user instance

        Raises:
            django.core.exceptions.ValidationError: When any of the values is not valid
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)
