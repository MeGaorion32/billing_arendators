from django.db import models

# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from api.models import BaseModel
from users.models import User

class Apartment(BaseModel):
    # user = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     verbose_name=_('Пользователь'),
    #     related_name='apartments'
    # )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_apartments',
        verbose_name=_('Владелец')
    )
    renter = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='rented_apartments',
        verbose_name=_('Арендатор')
    )
    name = models.CharField(
        _('Название объекта'),
        max_length=255
    )
    phone = models.CharField(
        _('Телефон объекта'),
        max_length=20
    )
    address = models.TextField(
        _('Адрес объекта')
    )
    date_first = models.CharField(
        _('Дата начала'),
        max_length=100
    )
    date_end = models.CharField(
        _('Дата окончания'),
        max_length=100
    )

    def save(self, *args, **kwargs):
        # Проверяем, что объект не привязывается к нескольким арендаторам
        if self.renter and self.renter.role != User.Role.RENTER:
            raise ValidationError(_('Объект можно привязывать только к арендаторам'))
        
        # Проверяем, что владелец - клиент или админ
        if self.owner and self.owner.role not in [User.Role.CLIENT, User.Role.ADMIN]:
            raise ValidationError(_('Владельцем объекта может быть только клиент или администратор'))
        
        super().save(*args, **kwargs)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['renter'],
                condition=models.Q(renter__isnull=False),
                name='unique_renter_per_apartment'
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.owner.get_full_name()})"