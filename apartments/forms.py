# apartments/forms.py
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Apartment
from users.models import User
from communal_services.models import CommunalServiceType

class ApartmentForm(forms.ModelForm):
    selected_types = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        initial=''
    )
    
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

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        if self.request and self.request.user.is_client:
            self.fields['owner'].initial = self.request.user
            self.fields['owner'].widget = forms.HiddenInput()
        
        if self.instance.pk:
            initial_types = ','.join(str(t.id) for t in self.instance.communal_service_types.all())
            self.fields['selected_types'].initial = initial_types

    def clean_selected_types(self):
        data = self.cleaned_data['selected_types']
        if data:
            try:
                return [int(id) for id in data.split(',') if id]
            except ValueError:
                raise forms.ValidationError(_("Некорректный формат ID типов услуг"))
        return []