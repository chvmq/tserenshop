from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Введите email')
        if not username:
            raise ValueError('Введите username')

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    """Кастомная модель для пользователей"""

    class Meta:
        verbose_name = 'Пользователь(я)'
        verbose_name_plural = 'Пользователи'
        db_table = 'account'

    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=255, unique=True, verbose_name='Никнейм')
    date_registration = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    last_login = models.DateTimeField(verbose_name='Последнее посещение', auto_now=True)
    is_admin = models.BooleanField(default=False, verbose_name='Администратор')
    is_staff = models.BooleanField(default=False, verbose_name='Сотрудник')
    is_active = models.BooleanField(default=True, verbose_name='Онлайн')
    is_superuser = models.BooleanField(default=False, verbose_name='Супер администратор')

    first_name = models.CharField(verbose_name='Имя', max_length=255)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255)
    number = models.CharField(verbose_name='Номер телефона', max_length=30, blank=True, null=True)

    objects = AccountManager()

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = [
        'email'
    ]

    def __str__(self):
        return f'{self.username}'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Address(models.Model):
    """Адреса проживания пользователей"""

    user = models.ForeignKey(Account, on_delete= models.CASCADE)
    country = models.CharField(max_length=255, default='Russia')
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255, blank=True)
    district = models.CharField(max_length=255, blank=True, verbose_name='Район')
    house = models.CharField(max_length=255)
    apartment_number = models.CharField(max_length=255, verbose_name='Квартира', blank=True)

    def __str__(self):
        return f'Адресс пользователя {self.user.email} {self.user.first_name} {self.user.last_name}'

    class Meta:
        db_table = 'address'
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
