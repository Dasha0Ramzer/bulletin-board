from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Пользователь'),
        ('admin', 'Администратор'),
    )

    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    phone = models.CharField(max_length=35, verbose_name="Телефон", blank=True, null=True)
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user', verbose_name="Роль")
    image = models.ImageField(upload_to='users/avatars', blank=True, null=True, verbose_name="Аватарка")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"