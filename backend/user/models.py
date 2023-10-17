from django.contrib.auth.models import AbstractUser
from django.db import models
# from rest_framework_simplejwt.tokens import RefreshToken

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
    username = models.CharField(max_length=150, unique=True)
    role = models.CharField(max_length=15, choices=ROLES, default=USER)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
#    confirmation_code = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    # def tokens(self):
    #     refresh = RefreshToken.for_user(self)
    #     return ({
    #         'refresh': str(refresh),
    #         'access': str(refresh.access_token),
    #     })

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    def __str__(self):
        return self.username
