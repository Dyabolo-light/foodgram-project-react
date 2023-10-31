from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

USER = 'user'
ADMIN = 'admin'
SUPER_USER = 'super_user'

ROLES = (
    (USER, 'user'),
    (ADMIN, 'admin'),
    (SUPER_USER, 'super_user'),
)


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=254, unique=True, blank=False,
                              null=False)
    username = models.CharField(
        max_length=150, unique=True,
        validators=[UnicodeUsernameValidator()]
    )
    role = models.CharField(max_length=15, choices=ROLES, default=USER)
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    password = models.CharField(max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self):
        return self.role == 'ADMIN' or self.is_superuser

    def __str__(self):
        return self.username
