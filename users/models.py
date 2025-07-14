from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from api.models import BaseModel

class UserManager(BaseUserManager):
    """Кастомный менеджер для модели User без username."""
    
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Создает и сохраняет пользователя с email и паролем."""
        if not email:
            raise ValueError(_('Необходимо указать email'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Создает обычного пользователя."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Создает суперпользователя."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_superuser=True.'))

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser, BaseModel):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Администратор')
        CLIENT = 'CLIENT', _('Клиент')
        RENTER = 'RENTER', _('Арендатор')

    username = None  # Убираем username
    email = models.EmailField(
        _('email address'), 
        unique=True,
        help_text=_('Обязательное поле. Введите действительный email адрес.')
    )
    role = models.CharField(
        _('Роль'),
        max_length=50, 
        choices=Role.choices, 
        default=Role.CLIENT,
        help_text=_('Выберите роль пользователя в системе')
    )
    first_name = models.CharField(
        _('Имя'),
        max_length=150,
        blank=False,
        help_text=_('Обязательное поле. Введите имя пользователя.')
    )
    last_name = models.CharField(
        _('Фамилия'),
        max_length=150,
        blank=False,
        help_text=_('Обязательное поле. Введите фамилию пользователя.')
    )
    patronymic = models.CharField(
        _('Отчество'),
        max_length=150,
        blank=True,
        help_text=_('Введите отчество пользователя (необязательно)')
    )
    phone = models.CharField(
        _('Телефон'),
        max_length=20,
        blank=False,
        default='не указан',
        help_text=_('Обязательное поле. Введите контактный телефон.')
    )
    address = models.TextField(
        _('Адрес'),
        blank=False,
        default='не указан',
        help_text=_('Обязательное поле. Введите полный адрес.')
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'address']

    objects = UserManager()

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN
    
    @property
    def is_client(self):
        return self.role == self.Role.CLIENT
    
    @property
    def is_renter(self):
        return self.role == self.Role.RENTER

    def get_full_name(self):
        """Возвращает полное имя пользователя."""
        full_name = f"{self.last_name} {self.first_name}"
        if self.patronymic:
            full_name += f" {self.patronymic}"
        return full_name.strip()

