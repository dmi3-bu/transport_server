import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    # Дефолтные поля:
    # username
    # email
    # first_name
    # last_name
    # date_joined
    # last_login
    # is_active
    # is_staff
    # is_superuser
    # groups - связь
    # user_permissions - связь
    # Кастомные поля:
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    passport = models.CharField(max_length=10, default='')
    middle_name = models.CharField(max_length=50, default='')
    date_of_birth = models.DateField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    phone = models.CharField(max_length=10, null=False)


class Ticket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE, related_name='tickets')
    activated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True)
    image = models.ImageField(upload_to='images', null=True)
