# from django.contrib import admin
# from .models import Apartment

# class ApartmentAdmin(admin.ModelAdmin):  
#     list_display = ('owner', 'renter', 'name', 'phone', 'address', 'date_first', 'date_end')
#     list_filter = ('name', 'phone', 'address', 'date_first', 'date_end')
#     fieldsets = (
#         (None, {'fields': ('name', 'phone', 'address')}),
#         ('Other info', {'fields': ('owner', 'renter', 'date_first', 'date_end')}),        
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('owner', 'renter', 'name', 'phone', 'address', 'date_first', 'date_end'),
#         }),
#     )
#     search_fields = ('owner__email', 'renter_email', 'name', 'phone', 'address', 'date_first', 'date_end')
#     ordering = ('name',)

# admin.site.register(Apartment, ApartmentAdmin)



from django.contrib import admin
from .models import Apartment
from communal_services.models import CommunalServiceType

class CommunalServiceTypeInline(admin.TabularInline):
    model = Apartment.communal_service_types.through
    extra = 1
    verbose_name = "Тип коммунальной услуги"
    verbose_name_plural = "Типы коммунальных услуг"

class ApartmentAdmin(admin.ModelAdmin):  
    list_display = ('owner', 'renter', 'name', 'phone', 'address', 'date_first', 'date_end', 'display_service_types')
    list_filter = ('name', 'phone', 'address', 'date_first', 'date_end')
    fieldsets = (
        (None, {'fields': ('name', 'phone', 'address')}),
        ('Other info', {'fields': ('owner', 'renter', 'date_first', 'date_end')}),        
    )
    inlines = [CommunalServiceTypeInline]
    exclude = ('communal_service_types',)  # Исключаем стандартное поле
    
    def display_service_types(self, obj):
        return ", ".join([t.name for t in obj.communal_service_types.all()])
    display_service_types.short_description = "Типы услуг"

admin.site.register(Apartment, ApartmentAdmin)