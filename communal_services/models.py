from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from api.models import BaseModel
from apartments.models import Apartment

class CommunalService(BaseModel):
    name = models.CharField(_('Название услуги'), max_length=255)
    description = models.TextField(_('Описание услуги'), blank=True)

    class Meta:
        verbose_name = _('Коммунальная услуга')
        verbose_name_plural = _('Коммунальные услуги')
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class CommunalServiceType(BaseModel):
    name = models.CharField(_('Название типа'), max_length=255)
    description = models.TextField(_('Описание типа'), blank=True)
    communal_service = models.ForeignKey(
        CommunalService,
        on_delete=models.CASCADE,
        related_name='types',
        verbose_name=_('Коммунальная услуга')
    )
    objects = models.ManyToManyField(
        Apartment,
        related_name='communal_service_types',
        verbose_name=_('Объекты'),
        blank=True
    )
    division_by_tariff = models.BooleanField(
        _('Деление по тарифам'),
        default=False
    )
    had_general_tariff = models.BooleanField(
        _('Общий тариф'),
        default=False
    )
    had_parent = models.BooleanField(
        _('Родительский тип'),
        default=False
    )
    parent_type = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='child_types',
        verbose_name=_('Родительский тип'),
        limit_choices_to={'division_by_tariff': True}
    )
    tariff_1 = models.CharField(
        _('Тариф 1 (Пик)'),
        max_length=100,
        blank=True
    )
    tariff_2 = models.CharField(
        _('Тариф 2 (Ночь)'),
        max_length=100,
        blank=True
    )
    tariff_3 = models.CharField(
        _('Тариф 3 (Полупик)'),
        max_length=100,
        blank=True
    )
    default_tariff = models.CharField(
        _('Норма по умолчанию'),
        max_length=100,
        blank=True
    )
    general_tariff = models.CharField(
        _('Общий тариф'),
        max_length=100,
        blank=True
    )

    class Meta:
        verbose_name = _('Тип коммунальной услуги')
        verbose_name_plural = _('Типы коммунальных услуг')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.communal_service})"

    def clean(self):
        if self.division_by_tariff and (self.had_general_tariff or self.had_parent):
            raise ValidationError(_('При выборе "Деление по тарифам" другие варианты должны быть отключены'))
        
        if self.had_general_tariff and (self.division_by_tariff or self.had_parent):
            raise ValidationError(_('При выборе "Общий тариф" другие варианты должны быть отключены'))
        
        if self.had_parent and (self.division_by_tariff or self.had_general_tariff):
            raise ValidationError(_('При выборе "Родительский тип" другие варианты должны быть отключены'))
        
        if self.had_parent and not self.parent_type:
            raise ValidationError(_('Необходимо выбрать родительский тип'))
        
        # if self.division_by_tariff and not all([self.tariff_1, self.tariff_2, self.tariff_3, self.default_tariff]):
        #     raise ValidationError(_('Для типа с делением по тарифам необходимо заполнить все тарифы'))
        
        if self.had_general_tariff and not all([self.general_tariff, self.default_tariff]):
            raise ValidationError(_('Для типа с общим тарифом необходимо заполнить оба поля'))
        
        if self.had_parent and not self.default_tariff:
            raise ValidationError(_('Для типа с родительским типом необходимо указать норму по умолчанию'))