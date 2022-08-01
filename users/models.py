from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_superuser(self, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_dispatch", True)
        extra_fields.setdefault("is_technician", True)
        extra_fields.setdefault("is_manager", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must is_staff True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must is_superuser True")

    #def create_dispatch(self, password, )