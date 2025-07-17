from django.contrib import admin
from .models import CommunalService, CommunalServiceType

class CommunalServiceAdmin(admin.ModelAdmin):  
    list_display = ('name', 'description')
    list_filter = ('name', 'description')
    fieldsets = (
        (None, {'fields': ('name', 'description')}),            
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'description'),
        }),
    )
    search_fields = ('name', 'description')
    ordering = ('name',)

admin.site.register(CommunalService, CommunalServiceAdmin)


class CommunalServiceTypeAdmin(admin.ModelAdmin): 
    list_display = ('id', 'name', 'description', 'communal_service', 'division_by_tariff', 'had_general_tariff', 
                    'had_parent', 'parent_type', 'tariff_1', 'tariff_2', 'tariff_3', 'default_tariff', 'general_tariff')
    list_filter = ('name', 'description', 'division_by_tariff', 'had_general_tariff', 'had_parent', 
                   'tariff_1', 'tariff_2', 'tariff_3', 'default_tariff', 'general_tariff')
    fieldsets = (
        (None, {'fields': ('name', 'description', 'communal_service', 'division_by_tariff', 'had_general_tariff')}),    
        ('Тарифы', {'fields': ('tariff_1', 'tariff_2', 'tariff_3', 'default_tariff', 'general_tariff')}),         
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'description', 'communal_service', 'division_by_tariff', 'had_general_tariff',
                       'had_parent', 'parent_type', 'tariff_1', 'tariff_2', 'tariff_3', 'default_tariff', 'general_tariff'),
        }),
    )
    search_fields = ('name', 'description')
    ordering = ('name',)

admin.site.register(CommunalServiceType, CommunalServiceTypeAdmin)