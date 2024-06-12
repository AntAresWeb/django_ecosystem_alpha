import core.constants as const
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Имя пользователя обязательно.')

        if email is None:
            raise TypeError('Электронная почта обязательна.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Нужно обязательно указать пароль.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractUser):
    email = models.EmailField(
        max_length=const.LENGTH_STRING_254,
        unique=True,
        verbose_name='E-mail пользователя',
        error_messages={
            'unique': ('Такой e-mail уже используеется другим пользователем.'),
        },
    )
    username = models.CharField(
        max_length=const.LENGTH_STRING_100,
        unique=True,
        verbose_name='Логин пользователя',
        error_messages={
            'unique': ('Пользователь с таким логином уже существует.'),
        },
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Имя пользователя содержит недопустимые символы',
            ),
        ]
    )
    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('username',)
        unique_together = ('username', 'email',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
