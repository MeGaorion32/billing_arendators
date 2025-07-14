from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Apartment
from users.models import User

class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ['owner', 'name', 'phone', 'address', 'date_first', 'date_end']
        widgets = {
            'owner': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date_first': forms.TextInput(attrs={'class': 'form-control'}),
            'date_end': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'owner': _('Владелец объекта'),
            'name': _('Название объекта'),
            'phone': _('Телефон объекта'),
            'address': _('Адрес объекта'),
            'date_first': _('Дата начала'),
            'date_end': _('Дата окончания'),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        # Если пользователь - клиент, устанавливаем текущего пользователя как владельца
        if self.request and self.request.user.is_client:
            self.fields['owner'].initial = self.request.user
            self.fields['owner'].widget = forms.HiddenInput()