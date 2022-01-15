from django.contrib.auth.models import AbstractUser
import datetime

from services.users.managers import UserManager

class UserModel(AbstractUser):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    is_staff: bool
    is_active: bool
    date_joined: datetime.datetime

    objects: UserManager
