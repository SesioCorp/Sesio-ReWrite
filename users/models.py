from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, password, **extra_fields):
        """Create and save a User with the given email and password."""
        user = self.model(**extra_fields)
        user.password_updated = timezone.now().date()
        user.set_password(password)
        user.save(using=self._db)
        return user

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
        return self._create_user(password, **extra_fields)

    def create_dispatch(self, password=None, **extra_fields):
        """Create dispatch user"""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_dispatch", True)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(password, **extra_fields)

    def create_technician(self, password=None, **extra_fields):
        """Create technician user"""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_technician", True)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(password, **extra_fields)

    def create_manager(self, password=None, **extra_fields):
        """Create manager user"""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_manager", True)
        return self._create_user(password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    is_manager = models.BooleanField(default = False)
    is_dispatch = models.BooleanField(default = False)
    is_technician = models.BooleanField(default = False)

    objects = UserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return "-- %s" % (self.get_full_name())

