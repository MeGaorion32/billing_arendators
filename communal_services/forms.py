from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import CommunalService, CommunalServiceType


class CommunalServiceForm(forms.ModelForm):
    class Meta:
        model = CommunalService
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# class CommunalServiceTypeForm(forms.ModelForm):
#     class Meta:
#         model = CommunalServiceType
#         fields = '__all__'
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#             'division_by_tariff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#             'had_general_tariff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#             'had_parent': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#             'parent_type': forms.Select(attrs={'class': 'form-control'}),
#             'tariff_1': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
#             'tariff_2': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
#             'tariff_3': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
#             'default_tariff': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
#             'general_tariff': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
#         }

#     def __init__(self, *args, **kwargs):
#         self.communal_service = kwargs.pop('communal_service', None)
#         super().__init__(*args, **kwargs)

#         if self.communal_service:
#             self.fields['parent_type'].queryset = CommunalServiceType.objects.filter(
#                 communal_service=self.communal_service,
#                 division_by_tariff=True
#             ).exclude(pk=getattr(self.instance, 'pk', None))

#         # Устанавливаем начальные значения для всех полей
#         if self.instance.pk:
#             self.fields['tariff_1'].initial = self.instance.tariff_1
#             self.fields['tariff_2'].initial = self.instance.tariff_2
#             self.fields['tariff_3'].initial = self.instance.tariff_3
#             self.fields['default_tariff'].initial = self.instance.default_tariff
#             self.fields['general_tariff'].initial = self.instance.general_tariff

#     def clean(self):
#         cleaned_data = super().clean()
#         had_parent = cleaned_data.get('had_parent')
#         parent_type = cleaned_data.get('parent_type')
#         division = cleaned_data.get('division_by_tariff')
#         general = cleaned_data.get('had_general_tariff')

#         if had_parent and not parent_type:
#             raise forms.ValidationError(_('Необходимо выбрать родительский тип'))
        
#         if not (division or general or had_parent):
#             raise ValidationError(_('Необходимо выбрать один из типов тарификации'))

#         return cleaned_data

class CommunalServiceTypeForm(forms.ModelForm):
    class Meta:
        model = CommunalServiceType
        fields = ['name', 'description', 'division_by_tariff', 
                 'had_general_tariff', 'had_parent', 'parent_type',
                 'tariff_1', 'tariff_2', 'tariff_3', 'default_tariff',
                 'general_tariff']
        exclude = []  # Все поля, кроме тех, что определены ниже
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'division_by_tariff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'had_general_tariff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'had_parent': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'parent_type': forms.Select(attrs={'class': 'form-control'}),
            'tariff_1': forms.TextInput(attrs={'class': 'form-control'}),
            'tariff_2': forms.TextInput(attrs={'class': 'form-control'}),
            'tariff_3': forms.TextInput(attrs={'class': 'form-control'}),
            'default_tariff': forms.TextInput(attrs={'class': 'form-control'}),
            'general_tariff': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.communal_service = kwargs.pop('communal_service', None)
        super().__init__(*args, **kwargs)

        instance = kwargs.get('instance')
        
        # Всегда инициализируем queryset для parent_type
        if self.communal_service:
            self.fields['parent_type'].queryset = CommunalServiceType.objects.filter(
                communal_service=self.communal_service,
                division_by_tariff=True
            ).exclude(pk=getattr(instance, 'pk', None))

            if not self.fields['parent_type'].queryset.exists():
                self.fields['had_parent'].widget.attrs['disabled'] = True
                self.fields['had_parent'].help_text = _('Нет доступных родительских типов')

        # Для существующего экземпляра
        if instance:
            if instance.division_by_tariff:
                self.fields['division_by_tariff'].initial = True
                self.fields['tariff_1'].initial = instance.tariff_1
                self.fields['tariff_2'].initial = instance.tariff_2
                self.fields['tariff_3'].initial = instance.tariff_3
                self.fields['default_tariff'].initial = instance.default_tariff
            elif instance.had_general_tariff:
                self.fields['had_general_tariff'].initial = True
                self.fields['general_tariff'].initial = instance.general_tariff
                self.fields['default_tariff'].initial = instance.default_tariff
            elif instance.had_parent:
                self.fields['had_parent'].initial = True
                self.fields['parent_type'].initial = instance.parent_type
                self.fields['tariff_1'].initial = instance.tariff_1
                self.fields['tariff_2'].initial = instance.tariff_2
                self.fields['tariff_3'].initial = instance.tariff_3
                self.fields['default_tariff'].initial = instance.default_tariff


        if not self.instance.pk:
            # self.fields['parent_type'] = forms.ModelChoiceField(
            #     queryset=CommunalServiceType.objects.none(),
            #     required=False,
            #     widget=forms.Select(attrs={'class': 'form-control'}),
            #     label=_('Родительский тип')
            # )
             
            self.fields['tariff_1'] = forms.CharField(
                required=False,
                widget=forms.TextInput(attrs={'class': 'form-control'}),
                label=_('Тариф 1 (Пик)')
            )
            self.fields['tariff_2'] = forms.CharField(
                required=False,
                widget=forms.TextInput(attrs={'class': 'form-control'}),
                label=_('Тариф 2 (Ночь)')
            )
            self.fields['tariff_3'] = forms.CharField(
                required=False,
                widget=forms.TextInput(attrs={'class': 'form-control'}),
                label=_('Тариф 3 (Полупик)')
            )
            self.fields['default_tariff'] = forms.CharField(
                required=False,
                widget=forms.TextInput(attrs={'class': 'form-control'}),
                label=_('Норма по умолчанию')
            )
            self.fields['general_tariff'] = forms.CharField(
                required=False,
                widget=forms.TextInput(attrs={'class': 'form-control'}),
                label=_('Общий тариф')
            )

            if self.communal_service:
                parent_types = CommunalServiceType.objects.filter(
                    communal_service=self.communal_service,
                    division_by_tariff=True
                )
                self.fields['parent_type'].queryset = parent_types
                if not parent_types.exists():
                    self.fields['had_parent'].widget.attrs['disabled'] = True
                    self.fields['had_parent'].help_text = _('Нет доступных родительских типов')
        else:
            if self.instance.division_by_tariff:
                self.fields['tariff_1'] = forms.CharField(
                    initial=self.instance.tariff_1,
                    widget=forms.TextInput(attrs={'class': 'form-control'}),
                    label=_('Тариф 1 (Пик)')
                )
                self.fields['tariff_2'] = forms.CharField(
                    initial=self.instance.tariff_2,
                    widget=forms.TextInput(attrs={'class': 'form-control'}),
                    label=_('Тариф 2 (Ночь)')
                )
                self.fields['tariff_3'] = forms.CharField(
                    initial=self.instance.tariff_3,
                    widget=forms.TextInput(attrs={'class': 'form-control'}),
                    label=_('Тариф 3 (Полупик)')
                )
                self.fields['default_tariff'] = forms.CharField(
                    initial=self.instance.default_tariff,
                    widget=forms.TextInput(attrs={'class': 'form-control'}),
                    label=_('Норма по умолчанию')
                )
            elif self.instance.had_general_tariff:
                self.fields['general_tariff'] = forms.CharField(
                    initial=self.instance.general_tariff,
                    widget=forms.TextInput(attrs={'class': 'form-control'}),
                    label=_('Общий тариф')
                )
                self.fields['default_tariff'] = forms.CharField(
                    initial=self.instance.default_tariff,
                    widget=forms.TextInput(attrs={'class': 'form-control'}),
                    label=_('Норма по умолчанию')
                )
            elif self.instance.had_parent:
                self.fields['parent_type'] = forms.ModelChoiceField(
                    initial=self.instance.parent_type,
                    queryset=CommunalServiceType.objects.filter(
                        communal_service=self.instance.communal_service,
                        division_by_tariff=True
                    ),
                    widget=forms.Select(attrs={'class': 'form-control'}),
                    label=_('Родительский тип')
                )
                self.fields['tariff_1'] = forms.CharField(
                    initial=self.instance.tariff_1,
                    widget=forms.TextInput(attrs={'class': 'form-control'}),
                    label=_('Тариф 1 (Пик)')
                )
                self.fields['tariff_2'] = forms.CharField(
                    initial=self.instance.tariff_2,
                    widget=forms.TextInput(attrs={'class': 'form-control'}),
                    label=_('Тариф 2 (Ночь)')
                )
                self.fields['tariff_3'] = forms.CharField(
                    initial=self.instance.tariff_3,
                    widget=forms.TextInput(attrs={'class': 'form-control'}),
                    label=_('Тариф 3 (Полупик)')
                )
                self.fields['default_tariff'] = forms.CharField(
                    initial=self.instance.default_tariff,
                    widget=forms.TextInput(attrs={'class': 'form-control'}),
                    label=_('Норма по умолчанию')
                )

    def clean(self):
        cleaned_data = super().clean()
        had_parent = cleaned_data.get('had_parent')
        parent_type = cleaned_data.get('parent_type')
        division = cleaned_data.get('division_by_tariff')
        general = cleaned_data.get('had_general_tariff')

        if had_parent and not parent_type:
            raise forms.ValidationError(_('Необходимо выбрать родительский тип'))
        
        if not (division or general or had_parent):
            raise ValidationError(_('Необходимо выбрать один из типов тарификации'))

        return cleaned_data