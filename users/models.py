from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.contrib.auth.models import BaseUserManager


# Create your models here.
def generate_photo_upload_path(instance, filename):
    profile = instance.user
    return f'files/profiles/{profile.pk}/{filename}'


class MyUserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name='aa', password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, full_name, password, **extra_fields)


class MyUser(AbstractUser):
    username = None
    full_name = models.CharField(max_length=250, blank=True)
    email = models.EmailField(unique=True)  # Ensure email is unique
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # remove 'email' from REQUIRED_FIELDS

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="myuser_set",
        related_query_name="myuser",
    )

    groups = models.ManyToManyField(
        Group,
        related_name="myuser_groups",
        related_query_name="myuser",
    )

    objects = MyUserManager()


class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='user_profile')
    photo = models.ImageField(blank=True, upload_to=generate_photo_upload_path)

    def __str__(self) -> str:
        return self.user.email
