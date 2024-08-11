from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name="Адрес электронной почты",
        unique=True
    )
    phone = models.CharField(
        max_length=35,
        verbose_name="Номер телефона",
        blank=True,
        null=True,
        help_text="Введите номер телефона"
    )
    country = models.CharField(
        verbose_name="Страна",
        max_length=50,
        blank=True,
        null=True,
        help_text="Введите страну")

    token = models.CharField(
        max_length=100,
        verbose_name='Токен',
        blank=True,
        null=True,
        help_text='Токен для авторизации'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
    