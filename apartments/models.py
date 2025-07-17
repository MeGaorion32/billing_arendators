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
    

    def get_communal_service_types_tree(self):
        from communal_services.models import CommunalServiceType
        all_types = CommunalServiceType.objects.filter(objects=self)
        return all_types

    
    def update_communal_service_types(self, type_ids):
        from communal_services.models import CommunalServiceType
        
        if not type_ids:
            self.communal_service_types.clear()
            return
        
        if isinstance(type_ids, str):
            type_ids = [int(id.strip()) for id in type_ids.split(',') if id.strip()]
        
        # Получаем существующие и новые ID
        current_ids = set(self.communal_service_types.values_list('id', flat=True))
        new_ids = set(type_ids)
        
        # Добавляем новые связи
        for type_id in new_ids - current_ids:
            try:
                service_type = CommunalServiceType.objects.get(id=type_id)
                self.communal_service_types.add(service_type)
            except CommunalServiceType.DoesNotExist:
                continue
        
        # Удаляем старые связи
        for type_id in current_ids - new_ids:
            try:
                service_type = CommunalServiceType.objects.get(id=type_id)
                self.communal_service_types.remove(service_type)
            except CommunalServiceType.DoesNotExist:
                continue
            
    # def update_communal_service_types(self, type_ids):
    #     from communal_services.models import CommunalServiceType
    #     from django.core.exceptions import ObjectDoesNotExist
        
    #     try:
    #         if isinstance(type_ids, str):
    #             type_ids = [int(id.strip()) for id in type_ids.split(',') if id.strip()]
    #         else:
    #             type_ids = list(map(int, type_ids))
            
    #         current_types = set(self.communal_service_types.values_list('id', flat=True))
    #         new_types = set(type_ids)
            
    #         # Добавляем новые связи
    #         for type_id in new_types - current_types:
    #             try:
    #                 service_type = CommunalServiceType.objects.get(id=type_id)
    #                 self.communal_service_types.add(service_type)
    #             except ObjectDoesNotExist:
    #                 continue
            
    #         # Удаляем старые связи
    #         for type_id in current_types - new_types:
    #             try:
    #                 service_type = CommunalServiceType.objects.get(id=type_id)
    #                 self.communal_service_types.remove(service_type)
    #             except ObjectDoesNotExist:
    #                 continue
    #     except (ValueError, TypeError) as e:
    #         print(f"Error updating communal service types: {e}")