from django.contrib import admin
from .models import Apartment

class ApartmentAdmin(admin.ModelAdmin):  
    list_display = ('owner', 'renter', 'name', 'phone', 'address', 'date_first', 'date_end')
    list_filter = ('name', 'phone', 'address', 'date_first', 'date_end')
    fieldsets = (
        (None, {'fields': ('name', 'phone', 'address')}),
        ('Other info', {'fields': ('owner', 'renter', 'date_first', 'date_end')}),        
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('owner', 'renter', 'name', 'phone', 'address', 'date_first', 'date_end'),
        }),
    )
    search_fields = ('owner__email', 'renter_email', 'name', 'phone', 'address', 'date_first', 'date_end')
    ordering = ('name',)

admin.site.register(Apartment, ApartmentAdmin)